"""Implements twitter."""

from utils_base import Log, Time, TimeFormat, TimeZoneOffset

log = Log('Twitter')


class TwitterActionerMixinHelpers:
    @staticmethod
    def _update_status(api, tweet_text, media_ids, in_reply_to_status_id):
        if len(media_ids) > 0:
            if in_reply_to_status_id:
                response = api.update_status(
                    tweet_text,
                    media_ids=media_ids,
                    in_reply_to_status_id=in_reply_to_status_id,
                )
            else:
                response = api.update_status(
                    tweet_text,
                    media_ids=media_ids,
                )
        else:
            if in_reply_to_status_id:
                response = api.update_status(
                    tweet_text, in_reply_to_status_id=in_reply_to_status_id
                )
            else:
                response = api.update_status(tweet_text)
        return response

    @staticmethod
    def _upload_media(api, image_files):
        media_ids = []
        for image_file in image_files:
            media_id = api.media_upload(image_file).media_id
            media_ids.append(media_id)
            log.info(
                f'Uploaded status image {image_file} to twitter as {media_id}',
            )
        return media_ids

    @staticmethod
    def _update_profile_description(api):
        date_with_timezone = TimeFormat(
            '%Y-%m-%d %H:%M:%S', TimeZoneOffset.LK
        ).stringify(Time.now())
        description = (
            f'Automatically updated at {date_with_timezone} (#SriLanka Time)'
        )
        api.update_profile(description=description)
        log.info(f'Updated profile description to: {description}')
