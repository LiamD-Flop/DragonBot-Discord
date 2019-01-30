import discord
from discord.ext import commands
import tools.discordembed as dmbd
import tools.checks as checks
import tools.supportsql as sql

class Support:

    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def report(self, ctx, *, report: str):
        if not checks.CheckInReport(ctx.message.author.id)[0]:
            msg = report
            if "'" in report:
                msg = ""
                for y in report:
                    if y == "'":
                        msg = msg+y+"'"
                    else:
                        msg = msg+y
            sql.CreateReport(u=ctx.message.author.id, r=msg)
            desc = "**Bug Reported By**\n" + ctx.message.author.name + "\n\n**Reported Bug**\n" + report
            debug = {'report',ctx.message.author.name, ctx.message.author.id}
            em = dmbd.reportembed(desc)
            channel = self.client.get_channel("430850664185200640")
            server = self.client.get_server("394503106571796491")
            developer = server.get_member("202112726502211586")
            await self.client.send_message(channel, embed=em)
            await self.client.send_message(developer, debug)
        else:
            desc = "You already have an open report. Close that one first to create a new report. (d!closereport)"
            em = dmbd.reportembed(desc)
            await self.client.say(embed=em)

    @commands.command(pass_context=True)
    async def claimreport(self, ctx, report: str):
        if checks.checkmod(ctx.message):
            reportinfo = sql.RespondReport(u=ctx.message.author.id, r=report)
            if reportinfo[0]:
                bugchan = self.client.get_channel("430850664185200640")
                if ctx.message.author.id == "202112726502211586":
                    Responder = "Flop | Author"
                else:
                    Responder = ctx.message.author.name.capitalize()
                user = await self.client.get_user_info(reportinfo[2])
                msg = "[Bug Responds] {} has claimed your report. This chat is now a Support Chat.".format(Responder)
                await self.client.send_message(bugchan, "Bug has been claimed by {}.".format(ctx.message.author.mention))
                await self.client.send_message(user, msg)
        else:
            msg = "You don't have permisssions to do this."
            em = dmbd.rankembed(msg)
            await self.client.say(embed=em)



def setup(client):
    client.add_cog(Support(client))
