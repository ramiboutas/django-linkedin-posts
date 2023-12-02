# django-linkedin-posts


## Set up

0. Get your Linkedin Access Token
[https://www.linkedin.com/developers/tools/oauth/token-generator](https://www.linkedin.com/developers/tools/oauth/token-generator)
1. Install from PyPI
```
python -m pip install django-linkedin-posts
```
2. Add the package to your settings INSTALLED_APPS
```python

INSTALLED_APPS = [
    ...
    "django_linkedin_posts",
    ...
]
```
3. Add the following setting variables

```python
## thid-party apps

# django-linkedin-posts (our app)
import os
from dotenv import load_dotenv # python-dotenv

load_dotenv() 

LINKEDIN_AUTHOR_TPYE = "organization" # "organization" or "person"
LINKEDIN_AUTHOR_ID = os.environ.get("LINKEDIN_AUTHOR_ID")
LINKEDIN_ACCESS_TOKEN = os.environ.get("LINKEDIN_ACCESS_TOKEN")

## The following keys are not needed at the moment
## But they are planned to be used.
## For example for updating the Access Token using the Refresh Token
# LINKEDIN_CLIENT_ID = os.environ.get("LINKEDIN_CLIENT_ID")
# LINKEDIN_CLIENT_SECRET = os.environ.get("LINKEDIN_CLIENT_SECRET") 
# LINKEDIN_REFRESH_TOKEN = os.environ.get("LINKEDIN_REFRESH_TOKEN") 

```

## Usage

### Create a simple Post

```python
from django_linkedin_posts.models import Post

# create a post instance in the db
post = Post.objects.create(
    comment="Hi, this is me publishing a post using django-linkedin-posts"
)

# share it in Linkedin 
post.share()


```



### Create a poll with options 

```python
from django_linkedin_posts.models import create_poll_with_options

# create a poll with its options. 
p = create_poll_with_options("hello", "What's up?", ["good", "bad"])

# share it
p.share()


```