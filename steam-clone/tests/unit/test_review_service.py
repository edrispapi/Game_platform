"""Unit tests for Review Service highlights."""
import os
import sys

import pytest
from fastapi.testclient import TestClient

# Ensure the services package is importable
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from services.review_service.app.main import app
from services.review_service.app import crud, models, schemas
from services.review_service.app.database import get_db


@pytest.fixture()
def review_client(db_session):
    """Test client bound to the in-memory SQLite session."""
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


def _create_review(db_session, **overrides):
    payload = schemas.ReviewCreate(
        user_id=overrides.get('user_id', 1),
        game_id=overrides.get('game_id', 1),
        rating=overrides.get('rating', 5),
        title=overrides.get('title', 'Great game'),
        content=overrides.get('content', 'A must play experience.'),
        is_positive=overrides.get('is_positive', True),
    )
    db_review = crud.create_review(db_session, payload)
    db_review.status = models.ReviewStatus.APPROVED.value
    db_review.helpful_votes = overrides.get('helpful_votes', 5)
    db_review.total_votes = overrides.get('total_votes', db_review.helpful_votes)
    db_session.commit()
    db_session.refresh(db_review)
    return db_review


def test_get_review_highlights_orders_by_helpfulness(db_session):
    """Ensure the CRUD helper returns approved reviews ordered by helpfulness and rating."""
    top_review = _create_review(db_session, helpful_votes=25, rating=5)
    secondary_review = _create_review(db_session, helpful_votes=10, rating=4)
    # Review without approval should be ignored
    pending_payload = schemas.ReviewCreate(
        user_id=3,
        game_id=2,
        rating=5,
        title='Pending',
        content='Needs approval',
        is_positive=True,
    )
    pending = crud.create_review(db_session, pending_payload)
    db_session.commit()

    highlights = crud.get_review_highlights(db_session, limit=5)

    assert [review.id for review in highlights] == [top_review.id, secondary_review.id]
    assert pending.id not in {review.id for review in highlights}


def test_review_highlights_endpoint_returns_serialised_data(review_client, db_session):
    """API endpoint should surface the same data as the CRUD helper."""
    top_review = _create_review(db_session, helpful_votes=40, rating=5, title='Top Review')
    _create_review(db_session, helpful_votes=15, rating=4, title='Runner Up')

    response = review_client.get('/api/v1/reviews/highlights?limit=2')
    assert response.status_code == 200

    payload = response.json()
    assert isinstance(payload, list)
    assert len(payload) == 2
    assert payload[0]['id'] == top_review.id
    assert payload[0]['helpful_votes'] == 40
    assert payload[0]['title'] == 'Top Review'
    assert payload[0]['status'] == models.ReviewStatus.APPROVED.value
