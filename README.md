# ParadiseBot
Paradise is an upcoming Discord Moderation Bot with tons of features!<br>
Invite to your server by clicking <a href="https://discord.com/oauth2/authorize?client_id=1099349759359201329&scope=bot&permissions=8589934591">here!</a> (Active 24/7)<br>
Warning: Some features may not work with Python 3.11 and later! (No support for DPY migration)
<br><br>
<h1>Features</h1>
[ ] = Mandatory, { } = Optional<br>
<br>
<b>Misc:</b><br>
invite : Sends the bot's Auth URL in chat.<br>
support : Link to the bot's home / support server<br>
source : Sends the bot's github repo in chat.<br>
uptime : Displays the application's uptime in chat.<br>
filesay [file] : Displays the contents of a file in chat (bot owner only).<br>
avatar [@user] : Displays the specified user's avatar in chat.<br>
echo [message] : Repeat whatever the user said in chat.<br>
serverinfo : Displays information about a guild. (name, member count, etc.)<br>
userinfo : Displays information about a user. (name, creation date, etc.)<br>
<br>
<b>Moderation:</b><br>
warn [@user] {reason} : Warns the specified user (auto ban after 5 warns).<br>
removewarn [@user] [number] : Removes the specified ammount of warns from the specified user.<br>
clearwarns [@user] : Clears all warnings from the specified user.<br>
viewwarns [@user] : Displays a user's warns in chat.<br>
ban [@user] : Bans the specified user.<br>
unban [user_id] : Unbans the specified user.<br>
kick [@user] : Kicks the specified user.<br>
purge [number] : Deletes the specified number of messages.<br>
mute [@user] [duration] {reason} : Mutes the specified user (mute role required).<br>
nuke : Nukes & recreates the channel the message was sent on (for chat cleanup).<br>
autonuke [#channel] [duration] : Sets up autonuke for the specified channel.<br>
<br>
<b>Server:</b><br>
setwelcome [#channel] [welcome message] : Configure the welcome event for your server.<br>
setverification [#channel] [@role] [message] : Configure the verification event for your server.<br>
agecheck [on / off] : Enables / Disables the Account Age Checker function for your server.<br>
invfilter [on / off] : Enables / Disables the Invite Checker function for your server.<br>
setslowmode [time] : Allows you to set a custom slowmode value for the text channel.<br>
<br>
<b>Other:</b><br>
help [command] : Displays all available info for a command (usage and description).
<br>
<h1>How to Setup</h1>
1. Open <b>main.py</b> and scroll all the way down.<br>
2. Replace <b>YOUR_TOKEN_HERE</b> with your bot's token.<br>
3. If you want to host the bot on your local machine run <b>deploy.bat</b>.<br>
4. Run <b>main.py</b>.<br>
<br>
<h2>Changelog (03.06.2023)</h2>
- Added `Auto Nuke`<br>
- Added `autonuke` command (Set up or turn off Auto Nuke)<br>
- Improved `nuke` command. (Now copies channel overwrites)<br>
- Modified `source` command.<br>
- Bot owner can bypass rate limits.<br>
<hr>
<br>
Made by <b>@juicychann</b><br>
Join our <a href="https://discord.gg/KYRGHm3Ccy">Discord Server</a> for support & additional information!<br>
More updates coming soon :)
