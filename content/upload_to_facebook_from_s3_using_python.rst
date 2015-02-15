:date: 2015-02-14 12:05:01
:tags: facebook,video,python,api,s3,aws,requests
:category: blog
:slug: upload-video-to-facebook-from-s3-using-python
:author: Ken Cochrane
:title: Uploading a Video to Facebook from AWS S3 using python

If you have some video files stored in Amazon S3 and you want to upload those
videos to a Facebook page, using their video API here is some python code that
I used recently.

I spent a good chunk of a day trying to get this too work, so I'm posting this
here to help anyone else who is trying to do the same.

This code isn't using any special facebook libraries it is just using normal
python along with the requests library. It should be a good enough example
to figure out how to do most things.

It is important to note that you will need a valid access token with correct
permissions in order to get this to work, and that isn't covered in this blog
post.

Another thing that is important to note, that this uses a different API host
then the rest of the facebook API. Instead of ``graph.facebook.com`` it uses
``graph-video.facebook.com``

- **Facebook Video API**: https://developers.facebook.com/docs/graph-api/reference/v2.2/user/videos/
- **Facebook Access Tokens**: https://developers.facebook.com/docs/facebook-login/access-tokens


Requirements:
-------------

.. code-block:: bash

   $ pip install requests requests-toolbelt


Code:
-----

.. code-block:: python

    import os
    import base64
    import requests
    from requests_toolbelt import MultipartEncoder
    import uuid
    import logging


    log = logging.getLogger(__name__)


    def download_file_to_tmp(source_url):
        """
        download `source_url` to /tmp return the full path, doing it in chunks so
        that we don't have to store everything in memory.
        """
        log.debug("download {0}".format(source_url))
        tmp_location = "/tmp/s3_downloads"

        # come up with a random name to avoid clashes.
        rand_name = str(uuid.uuid4().get_hex().lower()[0:6])

        local_filename = source_url.split('/')[-1]

        # get the extension if it has one
        if local_filename.count(".") > 0:
            ext = local_filename.split('.')[-1]
            tmp_filename = u"{0}.{1}".format(rand_name, ext)
        else:
            tmp_filename = u"{0}.mp4".format(local_filename)

        temp_media_location = os.path.join(tmp_location, tmp_filename)
        # make the temp directory
        if not os.path.exists(tmp_location):
            os.makedirs(tmp_location)

        r = requests.get(source_url, stream=True)
        log.debug("headers = {0}".format(r.headers))
        with open(temp_media_location, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
        log.debug("finished download to {0}".format(temp_media_location))
        return temp_media_location


    def remove_file(temp_file):
        """ Given a valid file path remove it """
        if os.path.exists(temp_file):
            os.remove(temp_file)


    def upload_file(video_url, page_id, poster_url, access_token,
                    description, title):
        """
        ``video_url``: this is where the video is in s3.
        ``page_id``:  me or a page_id for the page you want to post too.
        ``poster_url``:  the url to the poster (thumbnail) for this video
        ``access_token``: your facebook access token with permissions to upload
            to the page you want to post too.
        ``description``:  the description of the video you are posting.
        ``title``:  the title of the video you are posting
        """

        # download to data
        local_video_file = download_file_to_tmp(video_url)
        video_file_name = local_video_file.split("/")[-1]

        if video_file_name and video_file_name.count(".") == 0:
            log.debug("video_file_name has no ext {0}".format(video_file_name))
            # if it doesn't have an extension add one to it.
            video_file_name = "{0}.mp4".format(video_file_name)
            log.debug("video_file_name converted to {0}".format(video_file_name))

        # download to data
        local_poster_file = download_file_to_tmp(poster_url)

        # need to encode it.
        with open(local_poster_file, "rb") as image_file:
            poster_encoded_string = base64.b64encode(image_file.read())

        # need binary rep of this, not sure if this would do it

        # put it all together to post to facebook
        if page_id or page_id == 'me':
            path = 'me/videos'
        else:
            path = "{0}/videos".format(page_id)

        fb_url = "https://graph-video.facebook.com/{0}?access_token={1}".format(
                 path, access_token)

        log.debug("video_file = {0}".format(local_video_file))
        log.debug("thumb_file = {0}".format(local_poster_file))
        log.debug("start upload to facebook")

        # multipart chunked uploads
        m = MultipartEncoder(
            fields={'description': description,
                    'title': title,
                    'thumb': poster_encoded_string,
                    'source': (video_file_name, open(local_video_file, 'rb'))}
        )

        r = requests.post(fb_url, headers={'Content-Type': m.content_type}, data=m)

        if r.status_code == 200:
            j_res = r.json()
            facebook_video_id = j_res.get('id')
            log.debug("facebook_video_id = {0}".format(facebook_video_id))
        else:
            log.error("Facebook upload error: {0}".format(r.text))

        # delete the tmp files
        remove_file(local_video_file)
        remove_file(local_poster_file)

        return facebook_video_id
