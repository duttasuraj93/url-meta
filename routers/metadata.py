from fastapi import APIRouter, HTTPException
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import requests, json, re

router = APIRouter()

@router.get("/metadata", status_code=200)
def getMetadata(url: str = ''):

    try:
        driver = webdriver.Firefox()
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        title = get_title(soup)
        description = get_description(soup)
        image = get_image(soup)
        if image:
            image = validate_image_url(image, url)

        driver.close()

        return {
            "url": url,
            "title": title,
            "description": description,
            "image": image
        }
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail='Connection error')


def get_title(soup):

    title = soup.find('title')
    if title:
        return [title.string]

    title = soup.find("meta",  property="og:title")
    if title:
        return [title['content']]
    title = soup.find("meta", attrs={'name': 'og:title'})
    if title:
        return [title['content']]

    title = soup.find("meta",  property="twitter:title")
    if title:
        return [title['content']]
    title = soup.find("meta", attrs={'name': 'twitter:title'})
    if title:
        return [title['content']]

    title = soup.find("meta",  property="title")
    if title:
        return [title['content']]
    title = soup.find("meta", attrs={'name': 'title'})
    if title:
        return [title['content']]

    title = soup.find("meta",  property="Title")
    if title:
        return [title['content']]
    title = soup.find("meta", attrs={'name': 'Title'})
    if title:
        return [title['content']]

    return []


def get_description(soup):

    description = soup.find("meta",  property="og:description")
    if description:
        return [description['content']]
    description = soup.find("meta", attrs={'name': 'og:description'})
    if description:
        return [description['content']]

    description = soup.find("meta",  property="twitter:description")
    if description:
        return [description['content']]
    description = soup.find("meta", attrs={'name': 'twitter:description'})
    if description:
        return [description['content']]

    description = soup.find("meta",  property="description")
    if description:
        return [description['content']]
    description = soup.find("meta",  attrs={'name': 'description'})
    if description:
        return [description['content']]

    description = soup.find("meta",  property="Description")
    if description:
        return [description['content']]
    description = soup.find("meta", attrs={'name': 'Description'})
    if description:
        return [description['content']]

    return []


def get_image(soup):

    image = soup.find("meta",  property="og:image")

    if image:
        return [image['content']]
    image = soup.find("meta", attrs={'name': 'og:image'})
    if image:
        return [image['content']]

    image = soup.find("meta",  property="twitter:image")
    if image:
        return [image['content']]
    image = soup.find("meta", attrs={'name': 'twitter:image'})
    if image:
        return [image['content']]

    image = soup.find("meta",  property="msapplication-TileImage")
    if image:
        return [image['content']]
    image = soup.find("meta", attrs={'name': 'msapplication-TileImage'})
    if image:
        return [image['content']]

    image = soup.find("meta",  property="image")
    if image:
        return [image['content']]
    image = soup.find("meta", attrs={'name': 'image'})
    if image:
        return [image['content']]

    image = soup.find("meta",  property="Image")
    if image:
        return [image['content']]
    description = soup.find("meta", attrs={'name': 'Image'})
    if image:
        return [image['content']]

    return []


def validate_image_url(image, url):
    if not re.match('(?:http|ftp|https)://', image[0]):
        parsed_uri = urlparse(url)
        result = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
        return [result + image[0]]
    else:
        return image
