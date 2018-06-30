from ucsd_bisb_unofficial.models import Post

def test_post_model(session):
    post = Post(title='foo')

    session.add(post)
    session.commit()

    assert post.id > 0