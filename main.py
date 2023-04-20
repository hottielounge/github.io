from flask import Flask,jsonify,send_file
import requests
from io import BytesIO
BASE_FRIENDS_URL = "https://friends.roblox.com/v1/users"    
app = Flask(__name__)

@app.route("/social_stats/<userid>")
def get_social_status(userid):
    FOLLOWERS_URL = f"{BASE_FRIENDS_URL}/{userid}/followers"
    FRIENDS_URL = f"{BASE_FRIENDS_URL}//{userid}/friends"
    FOLLOWING_URL = f"{BASE_FRIENDS_URL}//{userid}/followings"
    user_follower_count = requests.get(f"{FOLLOWERS_URL}/count")
    user_friend_count = requests.get(f"{FRIENDS_URL}/count")
    user_following_count = requests.get(f"{FOLLOWING_URL}/count")
    print(user_follower_count.json(),user_following_count.json(),user_friend_count.json())
    return jsonify({"followersC":user_follower_count.json()["count"],"followingsC":user_following_count.json()["count"],"friendsC":user_friend_count.json()["count"]})
    
@app.route("/headimage/<userid>")
def get_user_image(userid):
    HEADSHOT_URL = f"https://thumbnails.roblox.com/v1/users/avatar?userIds={userid}&size=840x830&format=Png&isCircular=false"
    response = requests.get(HEADSHOT_URL)
    img = BytesIO(response.content)
    return send_file(img, mimetype='image/png')

@app.route("/rapandvalue/<userid>")
def get_rap_and_value(userid):
    request = requests.get(f'https://www.rolimons.com/playerapi/player/{userid}').json()
    player_value = request['value']
    player_rap = request['rap']
    print(player_rap,player_value)
    return jsonify({"rap":player_rap,"value":player_value})

@app.route("/getprimry/<userid>")
def get_fav_items(userid):
    PRIMARY_URL = f"https://groups.roblox.com/v1/users/{userid}/groups/primary/role"
    req = requests.get(PRIMARY_URL).json()
    group_link = f"https://www.roblox.com/groups/{req['group']['id']}"
    return jsonify({"group":req['group'],"link":group_link})
if __name__ == "__main__":
    app.run("0.0.0.0",8080)
