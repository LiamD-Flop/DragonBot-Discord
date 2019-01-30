import discord
from time import strftime
import urllib.parse as urlparse

def newembed(a, t=None, d=None, u=None, c=0xFFA700):
    em = discord.Embed(title=t, description=d, url=u, colour=c)
    em.set_footer(text="Powered by Vulcan | © Flop", icon_url="https://media.liamd.pw/img/vulcan.png")

    return em

def reportembed(d=None, c=0xFFA700):
    em = discord.Embed(title="Report", description=d, colour=c)
    em.set_footer(text="Powered by Vulcan | © Flop", icon_url="https://media.liamd.pw/img/vulcan.png")

    return em

def musicembed(d=None, c=0xFFA700):
    em = discord.Embed(title="Music", description=d, colour=c)
    em.set_footer(text="Powered by Vulcan | © Flop", icon_url="https://media.liamd.pw/img/vulcan.png")

    return em

def playerembed(p=None, c=0xFFA700):
    try:
        em=discord.Embed(title="Now Playing", colour=c)
        url_data = urlparse.urlparse(p.url)
        query = urlparse.parse_qs(url_data.query)
        video = query["v"][0]
        vimg = "https://i.ytimg.com/vi/{}/hqdefault.jpg".format(video)
        em.set_image(url=vimg)
        em.add_field(name="Song", value=p.title, inline=False)
        em.add_field(name="Uploaded by", value=p.uploader, inline=True)
        em.add_field(name="Length", value="{0[0]}m {0[1]}s".format(divmod(p.duration, 60)), inline=True)
        em.add_field(name="Uploaded On", value=p.upload_date, inline=True)
        em.add_field(name="Views", value="{:,}".format(p.views), inline=True)
        em.set_footer(text="Powered by Vulcan | © Flop", icon_url="https://media.liamd.pw/img/vulcan.png")
    except Exception as e:
        print(e)

    return em


def econembed(d=None, c=0xFFA700):
    em = discord.Embed(title="Economy", description=d, colour=c)
    em.set_footer(text="Powered by Vulcan | © Flop", icon_url="https://media.liamd.pw/img/vulcan.png")

    return em

def crewembed(d=None, c=0xFFA700):
    em = discord.Embed(title="Crews", description=d, colour=c)
    em.set_footer(text="Powered by Vulcan | © Flop", icon_url="https://media.liamd.pw/img/vulcan.png")

    return em

def rankembed(d=None, c=0xFFA700):
    em = discord.Embed(title="Groups", description=d, colour=c)
    em.set_footer(text="Powered by Vulcan | © Flop", icon_url="https://media.liamd.pw/img/vulcan.png")

    return em

def hackembed(d=None, c=0xFFA700):
    em = discord.Embed(title="Hack Terminal", description=d, colour=c)
    em.set_footer(text="Powered by Vulcan | © Flop", icon_url="https://media.liamd.pw/img/vulcan.png")

    return em

def casinoembed(d=None, c=0xFFA700):
    em = discord.Embed(title="Casino", description=d, colour=c)
    em.set_footer(text="Powered by Vulcan | © Flop", icon_url="https://media.liamd.pw/img/vulcan.png")

    return em

def banembed(d=None, c=0xFFA700):
    em = discord.Embed(title="Bans", description=d, colour=c)
    em.set_footer(text="Powered by Vulcan | © Flop", icon_url="https://media.liamd.pw/img/vulcan.png")

    return em

def infopage(t=None, d=None, c=0xFFA700):
    em = discord.Embed(title=t, description=d, colour=c)
    em.set_footer(text="Powered by Vulcan | © Flop", icon_url="https://media.liamd.pw/img/vulcan.png")

    return em
def infop(d=None, c=0xFFA700):
    em = discord.Embed(description=d, colour=c)
    em.set_footer(text="Powered by Vulcan | © Flop", icon_url="https://media.liamd.pw/img/vulcan.png")

    return em

def logembed(a, t=None, d=None, u=None, c=0xFFA700):
    author = a.name + '#' + a.discriminator
    em = discord.Embed(title=t, description=d, url=u, colour=c)
    em.set_author(name=author, icon_url=a.avatar_url)
    em.set_footer(text="Powered by Vulcan | © Flop" + strftime('%a %b %d, %Y at %I:%M %p'), icon_url="https://media.liamd.pw/img/vulcan.png")

    return em



def pingembed(a, t=None, d=None, u=None, c=0xFFA700):
    author = a
    em = discord.Embed(title=t, description=d, url=u, colour=c)
    em.set_author(name=author)

    return em

def userinfo(u=None, chan=None, c=0xFFA700):
    em=discord.Embed()
    em.set_author(name="Dragon Info")
    em.set_thumbnail(url=u.avatar_url)
    em.add_field(name="Name", value=u.name, inline=True)
    em.add_field(name="ID", value=u.id, inline=True)
    em.add_field(name="Created On", value=u.created_at, inline=True)
    em.add_field(name="Bot", value=u.bot, inline=True)
    em.set_footer(text="Powered by Vulcan | © Flop")

    return em

def rainbowgeneral(n=None, pt=None, k=None, s=None, m=None, x=None, sp=None, c=0xFFA700):
    desc = "General Stats " + n
    em=discord.Embed(title="Dragon R6S", description=desc)
    em.add_field(name="Playtime" , value=pt, inline=True)
    em.add_field(name="Kills", value=k, inline=True)
    em.add_field(name="Shots", value=s, inline=True)
    em.add_field(name="Matches", value=m, inline=True)
    em.add_field(name="xp", value=x, inline=True)
    em.add_field(name="Specials", value=sp, inline=True)
    em.set_footer(text="Powered by Vulcan | © Flop")

    return em

def serverinfo(n=None, pt=None, k=None, s=None, m=None, x=None, sp=None, c=0xFFA700):
    desc = "General Stats " + n
    em=discord.Embed(title="Dragon R6S", description=desc)
    em.add_field(name="Region" , value=pt, inline=True)
    em.add_field(name="Kills", value=k, inline=True)
    em.add_field(name="Shots", value=s, inline=True)
    em.add_field(name="Matches", value=m, inline=True)
    em.add_field(name="xp", value=x, inline=True)
    em.add_field(name="Specials", value=sp, inline=True)
    em.set_footer(text="Powered by Vulcan | © Flop")

    return em

def fortniteemb(n=None, st=None, pt=None, kd=None, m=None, pf=None, c=0xFFA700):
    desc = "{} Stats for {} on {}".format(st,n,pf)
    em=discord.Embed(title="Dragon R6S", description=desc)
    em.add_field(name="Playtime" , value=pt, inline=True)
    em.add_field(name="Kills", value=kd, inline=True)
    em.add_field(name="Matches", value=m, inline=True)
    em.set_footer(text="Powered by Vulcan | © Flop")

    return em
