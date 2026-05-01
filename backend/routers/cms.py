from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.orm import Session

from auth import require_admin
from database import get_db
from models import (
    CMSAchiever,
    CMSCategory,
    CMSContactSubmission,
    CMSEvent,
    CMSGalleryAlbum,
    CMSGalleryPhoto,
    CMSNews,
    CMSPageContent,
    User,
)
from schemas import (
    ContactSubmissionIn,
    EventCreateIn,
    EventUpdateIn,
    GalleryAlbumCreateIn,
    GalleryAlbumUpdateIn,
    GalleryPhotoCreateIn,
    GalleryPhotoUpdateIn,
    MarketingCategoryCreateIn,
    MarketingCategoryUpdateIn,
    NewsArticleCreateIn,
    NewsArticleUpdateIn,
    PageContentCreateIn,
    PageContentUpdateIn,
)

router = APIRouter()


def _slugify(value: str) -> str:
    normalized = "".join(ch.lower() if ch.isalnum() else "-" for ch in value.strip())
    normalized = "-".join(part for part in normalized.split("-") if part)
    return normalized or "item"


def _build_news_item(news: CMSNews) -> dict:
    return {
        "id": news.id,
        "title": news.title,
        "slug": news.slug,
        "excerpt": news.excerpt,
        "content": news.content,
        "featured_image_url": news.featured_image_url,
        "author_id": news.author_id,
        "status": news.status.value if hasattr(news.status, "value") else news.status,
        "views": news.views,
        "published_at": news.published_at.isoformat() if news.published_at else None,
        "created_at": news.created_at.isoformat(),
        "updated_at": news.updated_at.isoformat(),
        "category_id": news.category_id,
        "category_name": news.category.name if news.category else None,
        "gallery": [],
    }


def _build_event_item(event: CMSEvent) -> dict:
    return {
        "id": event.id,
        "title": event.title,
        "slug": event.slug,
        "description": event.description,
        "location": event.location,
        "start_date": event.start_date.isoformat(),
        "end_date": event.end_date.isoformat(),
        "featured_image_url": event.featured_image_url,
        "organizer_id": event.organizer_id,
        "capacity": event.capacity,
        "registered_count": event.registered_count,
        "status": event.status.value if hasattr(event.status, "value") else event.status,
        "created_at": event.created_at.isoformat(),
        "updated_at": event.updated_at.isoformat(),
        "gallery": [],
    }


def _build_category_item(category: CMSCategory) -> dict:
    return {
        "id": category.id,
        "name": category.name,
        "slug": category.slug,
        "description": category.description,
        "created_at": category.created_at.isoformat(),
        "updated_at": category.updated_at.isoformat(),
    }


def _build_album_item(album: CMSGalleryAlbum) -> dict:
    return {
        "id": album.id,
        "title": album.title,
        "description": album.description,
        "cover_image_url": album.cover_image_url,
        "category": album.category,
        "date": album.date,
        "display_order": album.display_order,
        "is_active": album.is_active,
        "created_at": album.created_at.isoformat(),
        "updated_at": album.updated_at.isoformat(),
        "photo_count": len(album.photos) if album.photos is not None else 0,
        "photos": [
            {
                "id": photo.id,
                "image_url": photo.image_url,
                "thumbnail_url": photo.thumbnail_url,
                "caption": photo.caption,
                "display_order": photo.display_order,
                "is_active": photo.is_active,
            }
            for photo in album.photos
        ],
    }


def _build_photo_item(photo: CMSGalleryPhoto) -> dict:
    return {
        "id": photo.id,
        "album_id": photo.album_id,
        "image_url": photo.image_url,
        "thumbnail_url": photo.thumbnail_url,
        "caption": photo.caption,
        "display_order": photo.display_order,
        "is_active": photo.is_active,
        "created_at": photo.created_at.isoformat(),
    }


def _build_page_item(page: CMSPageContent) -> dict:
    return {
        "id": page.id,
        "slug": page.slug,
        "title": page.title,
        "content": page.content,
        "is_active": page.is_active,
        "created_at": page.created_at.isoformat(),
        "updated_at": page.updated_at.isoformat(),
    }


@router.get("/cms/categories")
def list_categories(db: Session = Depends(get_db)):
    categories = db.query(CMSCategory).order_by(CMSCategory.name).all()
    return {"success": True, "data": [_build_category_item(category) for category in categories]}


@router.post("/cms/categories")
def create_category(
    body: MarketingCategoryCreateIn,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    slug = _slugify(body.name)
    counter = 1
    while db.query(CMSCategory).filter(CMSCategory.slug == slug).first():
        counter += 1
        slug = f"{_slugify(body.name)}-{counter}"

    category = CMSCategory(name=body.name, slug=slug, description=body.description)
    db.add(category)
    db.commit()
    db.refresh(category)
    return {"success": True, "data": _build_category_item(category)}


@router.put("/cms/categories/{category_id}")
def update_category(
    category_id: int,
    body: MarketingCategoryUpdateIn,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    category = db.query(CMSCategory).filter(CMSCategory.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    if body.name is not None:
        category.name = body.name
        category.slug = _slugify(body.name)
    if body.description is not None:
        category.description = body.description

    db.commit()
    db.refresh(category)
    return {"success": True, "data": _build_category_item(category)}


@router.delete("/cms/categories/{category_id}")
def delete_category(
    category_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    category = db.query(CMSCategory).filter(CMSCategory.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    db.delete(category)
    db.commit()
    return {"success": True, "message": "Category deleted"}


@router.get("/cms/news")
def list_news(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    status: Optional[str] = None,
    search: Optional[str] = None,
    category_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    query = db.query(CMSNews)

    if status:
        try:
            query = query.filter(CMSNews.status == status)
        except ValueError:
            pass

    if search:
        query = query.filter(
            CMSNews.title.ilike(f"%{search}%")
            | CMSNews.excerpt.ilike(f"%{search}%")
            | CMSNews.content.ilike(f"%{search}%")
        )

    if category_id:
        query = query.filter(CMSNews.category_id == category_id)

    total = query.count()
    items = query.order_by(CMSNews.published_at.desc().nullslast(), CMSNews.created_at.desc())
    items = items.offset((page - 1) * limit).limit(limit).all()

    return {
        "success": True,
        "data": [_build_news_item(item) for item in items],
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "pages": (total + limit - 1) // limit,
        },
    }


@router.get("/cms/news/{slug}")
def get_news_by_slug(slug: str, db: Session = Depends(get_db)):
    news = db.query(CMSNews).filter(CMSNews.slug == slug).first()
    if news is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="News article not found")
    return {"success": True, "data": _build_news_item(news)}


@router.post("/cms/news")
def create_news(
    body: NewsArticleCreateIn,
    request: Request,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    slug = _slugify(body.title)
    counter = 1
    while db.query(CMSNews).filter(CMSNews.slug == slug).first():
        counter += 1
        slug = f"{_slugify(body.title)}-{counter}"

    news = CMSNews(
        title=body.title,
        slug=slug,
        excerpt=body.excerpt,
        content=body.content,
        featured_image_url=body.featured_image_url,
        category_id=body.category_id,
        status=body.status,
        author_id=current_user.id,
    )
    db.add(news)
    db.commit()
    db.refresh(news)
    return {"success": True, "data": _build_news_item(news)}


@router.put("/cms/news/{news_id}")
def update_news(
    news_id: int,
    body: NewsArticleUpdateIn,
    request: Request,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    news = db.query(CMSNews).filter(CMSNews.id == news_id).first()
    if news is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="News article not found")

    if body.title is not None:
        news.title = body.title
    if body.excerpt is not None:
        news.excerpt = body.excerpt
    if body.content is not None:
        news.content = body.content
    if body.featured_image_url is not None:
        news.featured_image_url = body.featured_image_url
    if body.category_id is not None:
        news.category_id = body.category_id
    if body.status is not None:
        news.status = body.status

    db.commit()
    db.refresh(news)
    return {"success": True, "data": _build_news_item(news)}


@router.delete("/cms/news/{news_id}")
def delete_news(
    news_id: int,
    request: Request,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    news = db.query(CMSNews).filter(CMSNews.id == news_id).first()
    if news is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="News article not found")
    db.delete(news)
    db.commit()
    return {"success": True, "message": "News article deleted"}


@router.get("/cms/events")
def list_events(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    status: Optional[str] = None,
    upcoming: Optional[bool] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(CMSEvent)

    if status:
        try:
            query = query.filter(CMSEvent.status == status)
        except ValueError:
            pass

    if upcoming is not None:
        today = date.today()
        if upcoming:
            query = query.filter(CMSEvent.start_date >= today)
        else:
            query = query.filter(CMSEvent.start_date < today)

    if search:
        query = query.filter(
            CMSEvent.title.ilike(f"%{search}%")
            | CMSEvent.description.ilike(f"%{search}%")
            | CMSEvent.location.ilike(f"%{search}%")
        )

    total = query.count()
    items = query.order_by(CMSEvent.start_date.asc(), CMSEvent.created_at.desc())
    items = items.offset((page - 1) * limit).limit(limit).all()

    return {
        "success": True,
        "data": [_build_event_item(item) for item in items],
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "pages": (total + limit - 1) // limit,
        },
    }


@router.get("/cms/events/{slug}")
def get_event_by_slug(slug: str, db: Session = Depends(get_db)):
    event = db.query(CMSEvent).filter(CMSEvent.slug == slug).first()
    if event is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    return {"success": True, "data": _build_event_item(event)}


@router.post("/cms/events")
def create_event(
    body: EventCreateIn,
    request: Request,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    slug = _slugify(body.title)
    counter = 1
    while db.query(CMSEvent).filter(CMSEvent.slug == slug).first():
        counter += 1
        slug = f"{_slugify(body.title)}-{counter}"

    event = CMSEvent(
        title=body.title,
        slug=slug,
        description=body.description,
        location=body.location,
        start_date=body.start_date,
        end_date=body.end_date,
        featured_image_url=body.featured_image_url,
        capacity=body.capacity,
        status=body.status,
        organizer_id=current_user.id,
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return {"success": True, "data": _build_event_item(event)}


@router.put("/cms/events/{event_id}")
def update_event(
    event_id: int,
    body: EventUpdateIn,
    request: Request,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    event = db.query(CMSEvent).filter(CMSEvent.id == event_id).first()
    if event is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    if body.title is not None:
        event.title = body.title
    if body.description is not None:
        event.description = body.description
    if body.location is not None:
        event.location = body.location
    if body.start_date is not None:
        event.start_date = body.start_date
    if body.end_date is not None:
        event.end_date = body.end_date
    if body.featured_image_url is not None:
        event.featured_image_url = body.featured_image_url
    if body.capacity is not None:
        event.capacity = body.capacity
    if body.status is not None:
        event.status = body.status

    db.commit()
    db.refresh(event)
    return {"success": True, "data": _build_event_item(event)}


@router.delete("/cms/events/{event_id}")
def delete_event(
    event_id: int,
    request: Request,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    event = db.query(CMSEvent).filter(CMSEvent.id == event_id).first()
    if event is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    db.delete(event)
    db.commit()
    return {"success": True, "message": "Event deleted"}


@router.get("/cms/gallery/albums")
def list_gallery_albums(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db),
):
    query = db.query(CMSGalleryAlbum)
    if is_active is not None:
        query = query.filter(CMSGalleryAlbum.is_active == is_active)

    total = query.count()
    albums = query.order_by(CMSGalleryAlbum.display_order.asc(), CMSGalleryAlbum.created_at.desc())
    albums = albums.offset((page - 1) * limit).limit(limit).all()
    return {
        "success": True,
        "data": [_build_album_item(album) for album in albums],
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "pages": (total + limit - 1) // limit,
        },
    }


@router.post("/cms/gallery/albums")
def create_gallery_album(
    body: GalleryAlbumCreateIn,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    album = CMSGalleryAlbum(
        title=body.title,
        description=body.description,
        cover_image_url=body.cover_image_url,
        category=body.category,
        date=body.date,
    )
    db.add(album)
    db.commit()
    db.refresh(album)
    return {"success": True, "data": _build_album_item(album)}


@router.put("/cms/gallery/albums/{album_id}")
def update_gallery_album(
    album_id: int,
    body: GalleryAlbumUpdateIn,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    album = db.query(CMSGalleryAlbum).filter(CMSGalleryAlbum.id == album_id).first()
    if album is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gallery album not found")

    if body.title is not None:
        album.title = body.title
    if body.description is not None:
        album.description = body.description
    if body.cover_image_url is not None:
        album.cover_image_url = body.cover_image_url
    if body.category is not None:
        album.category = body.category
    if body.date is not None:
        album.date = body.date

    db.commit()
    db.refresh(album)
    return {"success": True, "data": _build_album_item(album)}


@router.delete("/cms/gallery/albums/{album_id}")
def delete_gallery_album(
    album_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    album = db.query(CMSGalleryAlbum).filter(CMSGalleryAlbum.id == album_id).first()
    if album is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gallery album not found")
    db.delete(album)
    db.commit()
    return {"success": True, "message": "Gallery album deleted"}


@router.get("/cms/gallery/albums/{album_id}/photos")
def list_gallery_photos(album_id: int, db: Session = Depends(get_db)):
    album = db.query(CMSGalleryAlbum).filter(CMSGalleryAlbum.id == album_id).first()
    if album is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gallery album not found")
    return {"success": True, "data": [_build_photo_item(photo) for photo in album.photos]}


@router.post("/cms/gallery/albums/{album_id}/photos")
def create_gallery_photo(
    album_id: int,
    body: GalleryPhotoCreateIn,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    album = db.query(CMSGalleryAlbum).filter(CMSGalleryAlbum.id == album_id).first()
    if album is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gallery album not found")

    photo = CMSGalleryPhoto(
        album_id=album_id,
        image_url=body.image_url,
        thumbnail_url=body.thumbnail_url,
        caption=body.caption,
        display_order=body.display_order or 0,
    )
    db.add(photo)
    db.commit()
    db.refresh(photo)
    return {"success": True, "data": _build_photo_item(photo)}


@router.put("/cms/gallery/photos/{photo_id}")
def update_gallery_photo(
    photo_id: int,
    body: GalleryPhotoUpdateIn,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    photo = db.query(CMSGalleryPhoto).filter(CMSGalleryPhoto.id == photo_id).first()
    if photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gallery photo not found")

    if body.image_url is not None:
        photo.image_url = body.image_url
    if body.thumbnail_url is not None:
        photo.thumbnail_url = body.thumbnail_url
    if body.caption is not None:
        photo.caption = body.caption
    if body.display_order is not None:
        photo.display_order = body.display_order

    db.commit()
    db.refresh(photo)
    return {"success": True, "data": _build_photo_item(photo)}


@router.delete("/cms/gallery/photos/{photo_id}")
def delete_gallery_photo(
    photo_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    photo = db.query(CMSGalleryPhoto).filter(CMSGalleryPhoto.id == photo_id).first()
    if photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gallery photo not found")
    db.delete(photo)
    db.commit()
    return {"success": True, "message": "Gallery photo deleted"}


@router.get("/cms/pages")
def list_pages(db: Session = Depends(get_db)):
    pages = db.query(CMSPageContent).order_by(CMSPageContent.slug).all()
    return {"success": True, "data": [_build_page_item(page) for page in pages]}


@router.get("/cms/pages/{slug}")
def get_page_by_slug(slug: str, db: Session = Depends(get_db)):
    page = db.query(CMSPageContent).filter(CMSPageContent.slug == slug).first()
    if page is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Page not found")
    return {"success": True, "data": _build_page_item(page)}


@router.post("/cms/pages")
def create_page(
    body: PageContentCreateIn,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    existing = db.query(CMSPageContent).filter(CMSPageContent.slug == body.slug).first()
    if existing is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Page slug must be unique")

    page = CMSPageContent(
        slug=body.slug,
        title=body.title,
        content=body.content,
        is_active=body.is_active,
    )
    db.add(page)
    db.commit()
    db.refresh(page)
    return {"success": True, "data": _build_page_item(page)}


@router.put("/cms/pages/{page_id}")
def update_page(
    page_id: int,
    body: PageContentUpdateIn,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    page = db.query(CMSPageContent).filter(CMSPageContent.id == page_id).first()
    if page is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Page not found")

    if body.title is not None:
        page.title = body.title
    if body.content is not None:
        page.content = body.content
    if body.is_active is not None:
        page.is_active = body.is_active

    db.commit()
    db.refresh(page)
    return {"success": True, "data": _build_page_item(page)}


@router.delete("/cms/pages/{page_id}")
def delete_page(
    page_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    page = db.query(CMSPageContent).filter(CMSPageContent.id == page_id).first()
    if page is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Page not found")
    db.delete(page)
    db.commit()
    return {"success": True, "message": "Page deleted"}


@router.get("/cms/achievers")
def list_achievers(
    is_active: Optional[bool] = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    sort_by: str = Query("display_order"),
    sort_order: str = Query("ASC"),
    db: Session = Depends(get_db),
):
    query = db.query(CMSAchiever)
    if is_active is not None:
        query = query.filter(CMSAchiever.is_active == is_active)

    if sort_by == "year":
        order_column = CMSAchiever.year
    else:
        order_column = CMSAchiever.display_order

    if sort_order.upper() == "DESC":
        query = query.order_by(order_column.desc())
    else:
        query = query.order_by(order_column.asc())

    items = query.limit(limit).all()
    return {"success": True, "data": [
        {
            "id": achiever.id,
            "name": achiever.name,
            "photo_url": achiever.photo_url,
            "achievement": achiever.achievement,
            "category": achiever.category,
            "year": achiever.year,
            "display_order": achiever.display_order,
            "is_active": achiever.is_active,
        }
        for achiever in items
    ]}


@router.post("/cms/contact")
def submit_contact(body: ContactSubmissionIn, db: Session = Depends(get_db)):
    contact = CMSContactSubmission(
        first_name=body.first_name,
        last_name=body.last_name,
        email=body.email,
        phone=body.phone,
        subject=body.subject,
        message=body.message,
    )
    db.add(contact)
    db.commit()
    return {"success": True, "message": "Contact request received"}
