# ═══════════════════════════════════════════
#   LINK BYPASSER BOT v2.1
#   Developed by Youname
#   200+ shorteners | cool UI | force-join
# ═══════════════════════════════════════════
BOT_TOKEN = "9046473119:AAHN2ImjzBHqqhAyfg_Mx954Fk-iPr8uYYE"
# ═══════════════════════════════════════════

import os
import sys
import re
import asyncio
import logging
import requests
from urllib.parse import urlparse, urljoin
from aiogram import Bot, Dispatcher, F, BaseMiddleware
from aiogram.filters import Command
from aiogram.types import (
    Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

DEVELOPER = "HEISENBERG"
BOT_NAME = "Link Bypasser Bot"
BOT_VERSION = "v2.1"

# ── Force-join config ──────────────────────
FORCE_CHANNEL_ID = -1004264694127
FORCE_CHANNEL_LINK = "https://t.me/heisebburgscript"
# ───────────────────────────────────────────

REQUEST_TIMEOUT = 15
MAX_REDIRECTS = 15
MAX_HTML_HOPS = 5
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/122.0.0.0 Safari/537.36"
)

SHORTENER_HOSTS = {
    # ── Classic general ──────────────────────
    "bit.ly", "tinyurl.com", "t.co", "goo.gl", "ow.ly", "is.gd",
    "buff.ly", "rebrand.ly", "cutt.ly", "shorturl.at", "rb.gy",
    "shorte.st", "adf.ly", "bc.vc", "ouo.io", "ouo.press",
    "shrinkme.io", "shrinkearn.com", "linkshrink.net", "adfoc.us",
    "za.gl", "za.uy", "gplinks.co", "gplinks.in", "droplink.co",
    "yoshort.in", "mdiskshortner.link", "clk.sh", "clicksfly.com",
    "try2link.com", "arolinks.com", "indianshortner.in",
    "urlshortx.com", "tnlink.in", "omg10.com", "gtlink.co",
    "filesdl.in", "filesdl.top", "filesdl.xyz", "filesdl.net",

    # ── More general ────────────────────────
    "tiny.cc", "lnkd.in", "t.ly", "short.io", "bl.ink", "v.gd",
    "soo.gd", "s.id", "x.co", "snip.ly", "snipurl.com", "clck.ru",
    "u.to", "qps.ru", "shorte.ru", "1url.com", "2.gy", "2ly.link",
    "shrtco.de", "shrturl.co", "shorturl.com", "shorturl.gg",
    "tiny.one", "tiny.pl", "tny.im", "tny.so", "trib.al", "tr.im",
    "v.ht", "vzt.link", "xurls.co", "y2u.be", "yep.it", "yourls.org",

    # ── Indian / Bollywood / file hosts ─────
    "gplinks.com", "gplinks.net", "gplinks.co.in", "gplink.in",
    "gplinks.me", "mdisk.me", "mdisk.pro", "mdisk.ws", "mdisk.link",
    "mdisklink.link", "mdisklinks.com", "mdiskpro.in",
    "shrinkme.ink", "shrinkme.click", "shrinkme.pro", "shrinkme.link",
    "shrinke.me", "shrinkforearn.in", "shrinkforearn.xyz",
    "indianshortner.com", "indianshortner.xyz", "indianshortner.net",
    "clicksfly.net", "clicksfly.in", "clicksfly.xyz",
    "urlshortx.com", "urlshortx.in", "urlshortx.xyz",
    "tnlink.com", "tnlink.xyz", "tnlink.net", "tnlink.in",
    "omg10.com", "omg10.in", "omg10.xyz",
    "gtlink.co", "gtlink.in", "gtlink.xyz",
    "yoshort.in", "yoshort.xyz", "yoshort.net",
    "try2link.in", "try2link.xyz", "try2link.net",
    "arolinks.in", "arolinks.xyz", "arolinks.net",
    "droplink.in", "droplink.xyz", "droplink.net",
    "mdiskshortner.link", "mdiskshortner.in", "mdiskshortner.xyz",

    # ── Link protectors / ad-gates ──────────
    "linkmake.in", "linkmake.xyz", "linkmake.co", "linkmake.net",
    "jiolink.in", "jiolink.xyz", "jiolink.co", "jio.link",
    "linkshortify.com", "linkshortify.in", "linkshortify.xyz",
    "linkpays.in", "linkpays.xyz", "linkpays.co",
    "linkfly.net", "linkfly.in", "linkfly.xyz",
    "linkvertise.com", "linkvertise.net", "linkvertise.de",
    "linkpays.com", "linkpays.net", "linkpays.in",
    "linkbox.to", "linkbox.in", "linkbox.xyz",
    "linkrex.net", "linkrex.in", "linkrex.xyz",
    "link1s.com", "link1s.in", "link1s.xyz",
    "link4win.net", "link4win.in", "link4win.xyz",
    "link5s.com", "link5s.in", "link5s.xyz",
    "earnlink.io", "earnlink.in", "earnlink.xyz",
    "earn4link.in", "earn4link.xyz", "earn4link.net",
    "flylink.in", "flylink.xyz", "flylink.net",
    "shortingly.me", "shortingly.in", "shortingly.xyz",
    "shortmoz.link", "shortmoz.in", "shortmoz.xyz",
    "upfiles.com", "upfiles.in", "upfiles.xyz",
    "upfilesurl.com", "upfilesurl.in", "upfilesurl.xyz",
    "urlsopen.com", "urlsopen.in", "urlsopen.xyz",
    "urlz.fr", "urlz.in", "urlz.xyz",
    "usercher.com", "usercher.in", "usercher.xyz",
    "vearn.in", "vearn.xyz", "vearn.net",
    "vexshort.in", "vexshort.xyz", "vexshort.net",
    "viralurl.com", "viralurl.in", "viralurl.xyz",
    "viralweb.net", "viralweb.in", "viralweb.xyz",
    "web1s.com", "web1s.in", "web1s.xyz",
    "zagl.me", "zagl.in", "zagl.xyz",
    "zshort.link", "zshort.in", "zshort.xyz",

    # ── Western ad-gates ────────────────────
    "adf.ly", "adfoc.us", "adfly.com", "adfly.in", "adfly.xyz",
    "sh.st", "shortest.pro", "shortest.in",
    "shrink-service.it", "shrink-service.in", "shrink-service.xyz",
    "short2win.com", "short2win.in", "short2win.xyz",
    "shortearn.eu", "shortearn.in", "shortearn.xyz",
    "shortz.link", "shortz.in", "shortz.xyz",
    "srt.am", "srt.in", "srt.xyz",
    "stfly.me", "stfly.in", "stfly.xyz",
    "swzz.xyz", "swzz.in", "swzz.net",
    "tii.ai", "tii.in", "tii.xyz",
    "tr.link", "tr.in", "tr.xyz",
    "url-zip.com", "url-zip.in", "url-zip.xyz",
    "urls.fyi", "urls.in", "urls.xyz",
    "ux9.de", "ux9.in", "ux9.xyz",
    "veryshort.link", "veryshort.in", "veryshort.xyz",
    "weadsy.com", "weadsy.in", "weadsy.xyz",

    # ── Cloud / file redirectors ────────────
    "drive.google.com", "docs.google.com", "dropbox.com",
    "mega.nz", "mega.io", "mediafire.com", "pixeldrain.com",
    "pixeldrain.dev", "1fichier.com", "gofile.io", "gofile.co",
    "anonfiles.com", "bayfiles.com", "file.io", "filebin.net",
    "wetransfer.com", "sendspace.com", "zippyshare.com",
    "solidfiles.com", "userscloud.com", "uptobox.com",
    "uploadhaven.com", "uploadrar.com", "uploadcloud.pro",
    "upload.ee", "uploadhub.to", "uploadship.com",
    "hubcloud.foo", "hubcloud.ink", "hubcloud.xyz",
    "hubdrive.space", "hubdrive.xyz", "hubdrive.co",
    "gdflix.dev", "gdflix.pro", "gdflix.xyz", "gdflix.in",
    "gdtot.pro", "gdtot.in", "gdtot.xyz",
    "filepress.pro", "filepress.in", "filepress.xyz",
    "filebee.xyz", "filebee.in", "filebee.net",
    "fastdl.app", "fastdl.in", "fastdl.xyz",
    "vcloud.zip", "vcloud.press", "vcloud.co",
}

URL_REGEX = re.compile(r"https?://[^\s\"'<>]+", re.IGNORECASE)

HTML_PATTERNS = [
    re.compile(r'<meta[^>]+http-equiv=["\']refresh["\'][^>]+content=["\'][^;]*;\s*url=([^"\']+)["\']', re.I),
    re.compile(r'url\s*[:=]\s*["\'](https?://[^"\']+)["\']', re.I),
    re.compile(r'href\s*=\s*["\'](https?://[^"\']+)["\']', re.I),
    re.compile(r'data-(?:url|href|link|target)\s*=\s*["\'](https?://[^"\']+)["\']', re.I),
    re.compile(r'window\.location(?:\.href)?\s*=\s*["\'](https?://[^"\']+)["\']', re.I),
    re.compile(r'location\.replace\s*\(\s*["\'](https?://[^"\']+)["\']', re.I),
]

dp = Dispatcher()


# ── Helpers ────────────────────────────────
def get_token() -> str:
    token = (BOT_TOKEN or "").strip() or (os.getenv("BOT_TOKEN") or "").strip()
    if not token:
        print("[ERROR] BOT_TOKEN khali hai.")
        sys.exit(1)
    return token


def is_url(text: str) -> bool:
    return bool(URL_REGEX.search(text or ""))


def extract_urls(text: str):
    return URL_REGEX.findall(text or "")


def is_shortener_host(host: str) -> bool:
    host = host.lower().lstrip("www.")
    return any(host == h or host.endswith("." + h) for h in SHORTENER_HOSTS)


def http_resolve(url: str):
    chain = [url]
    current = url
    try:
        for _ in range(MAX_REDIRECTS):
            r = requests.get(
                current,
                headers={"User-Agent": USER_AGENT},
                allow_redirects=False,
                timeout=REQUEST_TIMEOUT,
            )
            if r.status_code in (301, 302, 303, 307, 308):
                loc = r.headers.get("Location")
                if not loc:
                    break
                current = urljoin(current, loc)
                chain.append(current)
            else:
                break
        return current, chain, None
    except requests.exceptions.Timeout:
        return current, chain, "Timeout."
    except Exception as e:
        return current, chain, f"Error: {e}"


def find_embedded_link(url: str):
    try:
        r = requests.get(
            url,
            headers={"User-Agent": USER_AGENT},
            timeout=REQUEST_TIMEOUT,
            allow_redirects=True,
        )
        html = r.text or ""
        candidates = []
        for pat in HTML_PATTERNS:
            for m in pat.findall(html):
                candidates.append(m.strip())
        host = urlparse(url).netloc
        cleaned = []
        for c in candidates:
            c = c.replace("\\/", "/")
            if any(c.lower().endswith(x) for x in (".css", ".js", ".png", ".jpg", ".svg", ".ico")):
                continue
            if urlparse(c).netloc == host:
                continue
            cleaned.append(c)
        for c in cleaned:
            if not is_shortener_host(urlparse(c).netloc):
                return c
        return cleaned[0] if cleaned else None
    except Exception as e:
        logger.error(f"HTML extract error for {url}: {e}")
        return None


def smart_bypass(url: str):
    chain = [url]
    current = url

    current, http_chain, err = http_resolve(current)
    chain.extend(http_chain[1:])
    if err:
        return current, chain, err

    for _ in range(MAX_HTML_HOPS):
        host = urlparse(current).netloc
        if not is_shortener_host(host):
            break
        embedded = find_embedded_link(current)
        if not embedded or embedded == current:
            break
        if is_shortener_host(urlparse(embedded).netloc):
            embedded, inner_chain, _ = http_resolve(embedded)
            chain.extend(inner_chain[1:])
        chain.append(embedded)
        current = embedded

    if "?" in current:
        p = urlparse(current)
        cleaned = p._replace(query="", fragment="").geturl()
    else:
        cleaned = current

    return cleaned, chain, None


# ── Force-join middleware ─────────────────
async def is_member(bot: Bot, user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(FORCE_CHANNEL_ID, user_id)
        return member.status in ("member", "administrator", "creator")
    except Exception as e:
        logger.warning(f"get_chat_member failed for {user_id}: {e}")
        return False


class ForceJoinMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        user = getattr(event, "from_user", None)
        if not user:
            return await handler(event, data)

        if await is_member(data["bot"], user.id):
            return await handler(event, data)

        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📢 Join Channel", url=FORCE_CHANNEL_LINK)],
            [InlineKeyboardButton(text="✅ I Joined — Verify", callback_data="check_join")],
        ])
        text = (
            f"🔒 <b>Access Locked</b>\n\n"
            f"Bot use karne ke liye pehle channel join karo:\n"
            f"👉 {FORCE_CHANNEL_LINK}\n\n"
            f"Join ke baad <b>Verify</b> dabao."
        )

        if isinstance(event, Message):
            await event.answer(text, parse_mode="HTML", reply_markup=kb)
        elif isinstance(event, CallbackQuery):
            await event.message.answer(text, parse_mode="HTML", reply_markup=kb)
            await event.answer()
        return


dp.message.middleware(ForceJoinMiddleware())
dp.callback_query.middleware(ForceJoinMiddleware())


@dp.callback_query(F.data == "check_join")
async def check_join(cb: CallbackQuery):
    if await is_member(cb.bot, cb.from_user.id):
        await cb.message.edit_text(
            "✅ <b>Verified!</b>\n\nAb bot use kar sakte ho. Link bhejo.",
            parse_mode="HTML",
        )
    else:
        await cb.answer("❌ Abhi join nahi kiya. Join karke phir try karo.", show_alert=True)


# ── UI: start / help / hosts ──────────────
@dp.message(Command("start"))
async def cmd_start(message: Message):
    text = (
        f"╔══════════════════════════╗\n"
        f"   🔗 <b>{BOT_NAME}</b> {BOT_VERSION}\n"
        f"╚══════════════════════════╝\n\n"
        f"👨‍💻 <b>Dev:</b> {DEVELOPER}\n"
        f"🌐 <b>Hosts:</b> {len(SHORTENER_HOSTS)}+ shorteners\n\n"
        f"⚡ <b>Kaise use kare:</b>\n"
        f"• Short/ad link bhejo → real link mil jayega\n"
        f"• JS + meta-refresh redirects bhi handle hote hain\n\n"
        f"📋 <b>Commands:</b>\n"
        f"├ /resolve <code>&lt;url&gt;</code> — manual bypass\n"
        f"├ /hosts — supported shorteners\n"
        f"└ /help — guide\n\n"
        f"<i>Link bhejo, bypass ready hai 🚀</i>"
    )
    await message.answer(text, parse_mode="HTML")


@dp.message(Command("help"))
async def cmd_help(message: Message):
    text = (
        f"📖 <b>Help — {BOT_NAME}</b>\n\n"
        f"<b>Bypass ke 3 stages:</b>\n"
        f"1️⃣ HTTP 301/302 redirects\n"
        f"2️⃣ HTML <code>&lt;meta refresh&gt;</code> + <code>data-url</code>\n"
        f"3️⃣ Inline JS (<code>window.location</code>, <code>location.replace</code>)\n\n"
        f"<b>Commands:</b>\n"
        f"• /resolve <code>&lt;url&gt;</code>\n"
        f"• /hosts\n"
        f"• /start\n\n"
        f"⚠️ Sirf public links pe use karo."
    )
    await message.answer(text, parse_mode="HTML")


@dp.message(Command("hosts"))
async def cmd_hosts(message: Message):
    hosts = sorted(SHORTENER_HOSTS)
    chunks = []
    cur = []
    for h in hosts:
        cur.append(h)
        if len(cur) == 40:
            chunks.append(cur)
            cur = []
    if cur:
        chunks.append(cur)

    header = f"🌐 <b>Supported Hosts ({len(hosts)}):</b>\n\n"
    await message.answer(header, parse_mode="HTML")
    for i, chunk in enumerate(chunks):
        body = " • ".join(f"<code>{h}</code>" for h in chunk)
        await message.answer(body, parse_mode="HTML")


@dp.message(Command("resolve"))
async def cmd_resolve(message: Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2 or not is_url(parts[1]):
        await message.answer("❌ Usage: <code>/resolve &lt;url&gt;</code>", parse_mode="HTML")
        return
    await process_url(message, parts[1].strip())


@dp.message(F.text)
async def handle_message(message: Message):
    urls = extract_urls(message.text)
    if not urls:
        await message.answer(
            "🔗 <b>Link bhejo</b> bypass karne ke liye.\n\n"
            f"<i>Developed by {DEVELOPER}</i>",
            parse_mode="HTML",
        )
        return
    await process_url(message, urls[0])


async def process_url(message: Message, url: str):
    status = await message.answer(
        "⏳ <b>Resolving...</b>\n"
        "<i>Deep scan chal raha hai — redirects, JS, meta-refresh sab check ho rahe hain.</i>",
        parse_mode="HTML",
    )

    final, chain, err = smart_bypass(url)

    if err:
        await status.edit_text(
            f"❌ <b>Bypass failed</b>\n\n"
            f"🔗 <b>Input:</b> <code>{url}</code>\n"
            f"⚠️ <b>Reason:</b> {err}\n\n"
            f"<i>Developed by {DEVELOPER}</i>",
            parse_mode="HTML",
        )
        return

    chain_text = ""
    if len(chain) > 1:
        lines = "\n".join(f"{i+1}. <code>{u}</code>" for i, u in enumerate(chain[:10]))
        if len(chain) > 10:
            lines += f"\n<i>... +{len(chain) - 10} more</i>"
        chain_text = f"\n\n🔁 <b>Chain:</b>\n{lines}"

    if final == url:
        note = "\n\n⚠️ <i>Koi redirect nahi mila — direct URL hai ya server ne block kiya.</i>"
    elif is_shortener_host(urlparse(final).netloc):
        note = "\n\n⚠️ <i>Final link abhi bhi shortener hai — captcha/JS challenge ne roka. Browser me manually kholo.</i>"
    else:
        note = ""

    await status.edit_text(
        f"✅ <b>Bypassed!</b>\n\n"
        f"🔗 <b>Original:</b>\n<code>{url}</code>\n\n"
        f"🎯 <b>Final:</b>\n<code>{final}</code>"
        f"{chain_text}{note}\n\n"
        f"<i>Developed by {DEVELOPER}</i>",
        parse_mode="HTML",
        disable_web_page_preview=True,
    )
    logger.info(f"Resolved: {url} -> {final}")


async def main():
    token = get_token()
    logger.info(f"Token loaded: {token[:6]}...{token[-4:]}")
    print(f"[BOT STARTED] {BOT_NAME} {BOT_VERSION} by {DEVELOPER}")

    bot = Bot(token=token)
    try:
        me = await bot.get_me()
        logger.info(f"Bot: @{me.username}")
    except Exception as e:
        logger.error(f"Bot init error: {e}")
        sys.exit(1)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("[BOT STOPPED]")
