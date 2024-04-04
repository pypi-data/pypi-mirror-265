"""Implements twitter."""


import logging

from utils_twitter.Tweet import Tweet
from utils_twitter.TwitterActionerMixinHelpers import \
    TwitterActionerMixinHelpers as helpers

log = logging.getLogger(__name__)


class TwitterActionerMixin:
    def send(self, tweet: Tweet):
        media_ids = helpers._upload_media(
            self.api,
            tweet.image_file_path_list,
        )
        return helpers._update_status(
            self.api, tweet.text, media_ids, tweet.in_reply_to_status_id
        )

    def update_profile_description(self):
        helpers._update_profile_description(self.api)

    def update_profile_image(self, profile_image_file):
        log.debug(f'update_profile_image: {profile_image_file}')
        self.api.update_profile_image(profile_image_file)

    def update_banner_image(self, banner_image_file):
        log.debug(f'update_banner_image: {banner_image_file}')
        self.api.update_profile_banner(banner_image_file)
