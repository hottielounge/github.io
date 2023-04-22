from flask import Flask,jsonify,send_file,make_response
import requests
from io import BytesIO
import base64
from flask_cors import CORS
DOMAIN = "j2sh.co"
BASE_FRIENDS_URL = "https://friends.roblox.com/v1/users"    
app = Flask(__name__)
CORS(app)

@app.route("/social_stats/<userid>")
def get_social_status(userid,server=None):
    FOLLOWERS_URL = f"{BASE_FRIENDS_URL}/{userid}/followers"
    FRIENDS_URL = f"{BASE_FRIENDS_URL}//{userid}/friends"
    FOLLOWING_URL = f"{BASE_FRIENDS_URL}//{userid}/followings"
    user_follower_count = requests.get(f"{FOLLOWERS_URL}/count")
    user_friend_count = requests.get(f"{FRIENDS_URL}/count")
    user_following_count = requests.get(f"{FOLLOWING_URL}/count")
    followers_count = user_follower_count.json().get("count", 0)
    friends_count = user_friend_count.json().get("count", 0)
    followings_count = user_following_count.json().get("count", 0)
    if server:
        return {"followersC":followers_count, "followingsC":followings_count, "friendsC":friends_count}
    return jsonify({"followersC":followers_count, "followingsC":followings_count, "friendsC":friends_count})

    
@app.route("/headimage/<userid>")
def get_user_image(userid,server=None):
    HEADSHOT_URL = f"https://thumbnails.roblox.com/v1/users/avatar?userIds={userid}&size=420x420&format=Png&isCircular=false"
    response = requests.get(HEADSHOT_URL)
    response = requests.get(response.json()["data"][0]["imageUrl"])
    img = BytesIO(response.content)
    img_content = base64.b64encode(response.content).decode('utf-8')
    return f'data:image/png;base64,{img_content}'

@app.route("/rapandvalue/<userid>")
def get_rap_and_value(userid,server=None):
    request = requests.get(f'https://www.rolimons.com/playerapi/player/{userid}').json()
    if request["success"] == False:
        return f"<h1>Error: {request['message']} </h1>"
    player_value = request['value']
    player_rap = request['rap']
    if server:
        return {"rap":player_rap,"value":player_value}
    return jsonify({"rap":player_rap,"value":player_value})

@app.route("/getprimry/<userid>")
def get_fav_items(userid,server=None):
    PRIMARY_URL = f"https://groups.roblox.com/v1/users/{userid}/groups/primary/role"
    req = requests.get(PRIMARY_URL).json()
    if req == None:
      return "<h1>Error</h1>"

    if req['group'] == None:
      return "<h1>Error</h1>"
    group_link = f"https://www.roblox.com/groups/{req['group']['id']}"
    if server:
        return {"group":req['group'],"link":group_link}
    return jsonify({"group":req['group'],"link":group_link})

@app.route("/getusername/<userid>")
def get_username(userid,server=None):
    USERNAME_URL = f"https://users.roblox.com/v1/users/{userid}"
    response = requests.get(USERNAME_URL)
    if response.status_code == 200:
        data = response.json()
        if server:
            return {"username":data["name"],"display":data["displayName"]}
        return jsonify({"username":data["name"],"display":data["displayName"]})
    else:
        return "<h1>Error</h1>"

@app.route("/profile/<userid>")
def profile(userid):
    social_stats = get_social_status(userid, server=True)
    image_url = get_user_image(userid, server=True)
    username_display = get_username(userid, server=True)
    if username_display == "<h1>Error</h1>":
        return "<h1>Error: Not real user</h1>"
    svg_s = f"""
<svg xmlns="http://www.w3.org/2000/svg" width="550" height="180" xmlns:xlink="http://www.w3.org/1999/xlink">
  <foreignObject x="0" y="0" width="520" height="150">
    <div class="profile-header" xmlns="http://www.w3.org/1999/xhtml" style="background-color: #36393f;" >
      <link href="https://fonts.googleapis.com/css?family=GG+Gothic+L" rel="stylesheet" />
      <div class="profile-info" style="position: absolute; color: #fff; font-size: 20px; flex-basis: 100%;">
        <h1 class="profile-name" style="font-size: xx-large; position: relative; height: 140px; left: 150px; font-family: 'GG Gothic L', sans-serif;">{ username_display['username'] }</h1>
        <h1 class="profile-display" style="font-size: large; position: absolute; top: 40px; left: 150px; font-family: 'GG Gothic L', sans-serif;">@{ username_display['display'] }</h1>
      </div>
      <div class="profile-stats" style="position: absolute; font-size: 20px; order: 2; bottom: 50px; color: black; left: 150px;">
        <ul style="list-style-type: none; padding: 0; margin: 0;">
          <li style="display: inline-flex; align-items: center;">
            <div class="profile-count" id="friendsCount" style="margin-right: 5px; color: #ffffff;">{ social_stats['friendsC'] }</div>
            <a style="color: #ffffff; text-decoration: none;">
              <span class="profile-label" style="color: #999999; font-size: 12px; margin-bottom: 3px; height: 20px; right: 10px;">Friends</span>
            </a>
          </li>
          <li style="display: inline-flex; align-items: center;">
            <div class="profile-count" id="followersCount" style="margin-right: 5px; color: #ffffff;">{ social_stats['followersC'] }</div>
            <a style="color: #ffffff; text-decoration: none;">
              <span class="profile-label" style="color: #999999; font-size: 12px; margin-bottom: 3px; height: 20px; right: 10px;">Followers</span>
            </a>
          </li>
          <li style="display: inline-flex; align-items: center;">
            <div class="profile-count" id="followingCount" style="margin-right: 5px; color: #ffffff;">{ social_stats['followingsC'] }</div>
            <a style="color: #ffffff; text-decoration: none;">
              <span class="profile-label" style="color: #999999; font-size: 12px; margin-bottom: 3px; height: 20px; right: 10px;">Following</span>
            </a>
          </li>
        </ul>
      </div>
      <div class="profile-avatar" style="left: 550px;">
        <img class="uwu" src=" { image_url } " width="150" height="150" />
      </div>
    </div>
  </foreignObject>
  <script>
    const userid = {userid}
    const domain = '{DOMAIN}'
    setInterval(() => {{
        fetch(`${{domain}}/social_stats/${{userid}}`)
          .then(response => response.json())
          .then(data => {{
            // Update social stats UI elements with data
            document.getElementById('followersCount').innerHTML = data.followersC;
            document.getElementById('followingCount').innerHTML = data.followingsC;
            document.getElementById('friendsCount').innerHTML = data.friendsC;
          }})
          .catch();
        fetch(`${{domain}}/getusername/${{userid}}`)
              .then(response => response.json())
              .then(data => {{
                document.getElementsByClassName('profile-display').innerHTML = data.display
                document.getElementsByClassName('profile-name').innerHTML = data.username
              }})
              .catch();
        fetch(`${{domain}}/headimage/${{userid}}`)
              .then(response => response.text())
              .then(data => {{
                document.getElementsByClassName('uwu')[0].src = data;
              }})
              .catch();
          }}, 30000);
          
  </script>
    </svg>
    """
    response = make_response(svg_s)
    response.headers.set('Content-Type', 'image/svg+xml')
    return response
    


if __name__ == "__main__":
    app.run("0.0.0.0",8080)