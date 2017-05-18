Quick Cache Warmer
==================

This script utilizes Google Analytics to selectively warm the cache of your top visited pages. Easily set the script to run as a cron before your peak usage or after a site wide cache clear to ensure end-users are hitting cached content.


Installation/Setup
------------------

**Step 1: Install Dependencies**

Simply run `pip install -r requirements.txt`

**Step 2: Create a Google Service Account and Download the JSON Key**

First, create a [Google Service Account](https://developers.google.com/identity/protocols/OAuth2ServiceAccount#creatinganaccount). Then you will need to create a new JSON key or use an existing key if you already have one. The key will need to be moved to the project directory and be renamed to `key.json`.

For more information on Step 2 and 3, see the [Google Analytics Server-side Authorization documentation](https://ga-dev-tools.appspot.com/embed-api/server-side-authorization/).

**Step 3: Add the Google Service Account as a User to Google Analytics**

Find the `client_email` email address inside the `key.json` file and add the email as read-only user to the Google Analytics View.

**Step 4: Setup Environment Variables**

The script makes use of a `.env` file in the project directory. You can get started by copying the `.env-example` file to `.env`.

| Option | Example | Description |
| --- | --- | --- |
| `DOMAIN` | `DOMAIN=example.com` | Google Analytics API returns paths without a domain or protocol. This should be your main domain. |
| `PROTOCOL` | `PROTOCOL=https` | Google Analytics API returns paths without a domain or protocol. This should be `http` or `https`. |
| `THREADS` | `THREADS=5` | The number of threads to use. Limited to 10. |
| `DELAY` | `DELAY=500` | The delay in ms between URL requests. |
| `SMTP_SERVER` | `SMTP_SERVER=smtp.mailgun.org` | The SMTP server hostname. |
| `SMTP_USERNAME` | `SMTP_SERVER=username@hash.mailgun.org` | The SMTP server username. |
| `SMTP_PASSWORD` | `SMTP_SERVER=username@hash.mailgun.org` | The SMTP server password. |
| `SMTP_PORT` | `SMTP_PORT=587` | The SMTP server port. |
| `SMTP_FROM` | `SMTP_FROM=no-reply@example.com` | The SMTP server from address. If using [Mailgun](https://www.mailgun.com/), this likely will be the same as `SMTP_USERNAME`. |
| `SMTP_RECIPIENTS` | `SMTP_RECIPIENTS=email1@example.com` | The email addresses that the final report will be sent to. Multiple email address need to be separated with a comma. |
| `WEBHOOK` | `WEBHOOK=URL` | A Slack webhook URL, if this is set an email will not be sent. |


Usage
-----

**Google Analytics Crawler:**

```bash
python crawl.py -i 123456789 -c 10
```

**Sitemap.XML Crawler:**

```bash
python crawl.py -s http://example.com/sitemap.xml -c 100
```

**Arguments**

| Option | Description |
| --- | --- |
| `-i` or `--id` | The unique Google Analytics View ID. For more information about getting the View ID, see [this article](https://lucidpress.zendesk.com/hc/en-us/articles/207335356-Find-your-Google-Analytics-Tracking-ID-View-ID). |
| `-s` or `--sitemap` | The full web URL to Sitemap.XML file to crawl. This format should be use the [proper sitemap XML schema](http://www.sitemaps.org/protocol.html). |
| `-c` or `--count` | The number of pages to warm. For example, if you set this to 10, the warmer will crawl the top 10 visited pages according to Google Analytics. The script is limited to 1000 pages. |
