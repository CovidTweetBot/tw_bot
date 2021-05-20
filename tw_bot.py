import os

import click
import tweepy


class ImageStorage:
    def __init__(self, location):
        self._location = location

    @property
    def location(self):
        return os.path.abspath(self._location)

    def path(self, name):
        return os.path.join(self.location, name)

    def exists(self, name):
        return os.path.exists(self.path(name))

    def delete(self, name):
        name = self.path(name)
        # If the file or directory exists, delete it from the filesystem.
        try:
            if os.path.isdir(name):
                os.rmdir(name)
            else:
                os.remove(name)
        except FileNotFoundError:
            pass


class TwitterBot:
    def __init__(
        self,
        consumer_key: str,
        consumer_secret: str,
        access_token: str,
        access_token_secret: str,
        images_base_location: str,
    ):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self._api = tweepy.API(auth)
        self._image_storage = ImageStorage(images_base_location)

    def run(self, dataset: str) -> None:
        last_status = None
        regions = ("peru", "amazonas", "ancash", "apurimac", "arequipa")
        count_regions = len(regions)
        for index, region in enumerate(regions):
            image_filename = f"{dataset}/not_processed/{region}.png"
            if self._image_storage.exists(image_filename):
                # upload media/image
                media = self._api.media_upload(self._image_storage.path(image_filename))
                msg = f"{region.upper()}: Fallecidos por causas no violentas {index + 1}/{count_regions}"
                kwargs = {"status": msg, "media_ids": [media.media_id]}
                if last_status:
                    kwargs["in_reply_to_status_id"] = last_status.id
                last_status = self._api.update_status(**kwargs)
                # TODO: move image file instead of removing it ??
                # delete image already processed
                self._image_storage.delete(image_filename)


@click.command()
@click.option("--twitter_consumer_key", required=True, envvar="TWITTER_CONSUMER_KEY")
@click.option(
    "--twitter_consumer_secret", required=True, envvar="TWITTER_CONSUMER_SECRET"
)
@click.option("--twitter_access_token", required=True, envvar="TWITTER_ACCESS_TOKEN")
@click.option(
    "--twitter_access_token_secret", required=True, envvar="TWITTER_ACCESS_TOKEN_SECRET"
)
def main(
    twitter_consumer_key,
    twitter_consumer_secret,
    twitter_access_token,
    twitter_access_token_secret,
):
    bot = TwitterBot(
        consumer_key=twitter_consumer_key,
        consumer_secret=twitter_consumer_secret,
        access_token=twitter_access_token,
        access_token_secret=twitter_access_token_secret,
        images_base_location="./images",
    )
    bot.run("sinadef")
    # bot.run("vaccinations")


if __name__ == "__main__":
    main()
