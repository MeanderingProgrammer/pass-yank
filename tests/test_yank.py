from yank import Metadata, MetadataItem, parse_metadata


def test_full() -> None:
    username = MetadataItem(key="Username", value="user@example.com")
    user_id = MetadataItem(key="User Id", value="my-user-id")
    url = MetadataItem(key="url", value="*.amazon.com/*")

    metadata: Metadata = parse_metadata(
        "super-secret-password",
        "Username: user@example.com",
        "User Id: my-user-id",
        "url: *.amazon.com/*",
        "URL: https://amazon.com/some-url",
    )
    assert ["username", "user_id", "url"] == metadata.fields
    assert [username, user_id, url] == metadata.items

    assert username == metadata.get_first(["^user.*$", "^email.*$"])
    assert url == metadata.get_first(["url"])
    assert metadata.get_first(["amazon"]) is None
