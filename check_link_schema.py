from app.schemas.link_schema import LinkCreate

# Valid input
link = LinkCreate(
    target_url="https://example.com",
    user_id="550e8400-e29b-41d4-a716-446655440000",
)
print(link)

# Invalid URL
LinkCreate(
    target_url="not-a-url",
    user_id="550e8400-e29b-41d4-a716-446655440000",
)

# Invalid UUID
LinkCreate(
    target_url="https://example.com",
    user_id="invalid-uuid",
)
