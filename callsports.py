from flask import Flask, Response, request, session
import twilio.twiml
from SportAPI import SportAPI

app = Flask(__name__)
app.config.from_pyfile('application.cfg', silent=True)
app.secret_key = app.config['FLASK_SECRET_KEY']

sports = {
    1: 'soccer',
    2: 'tennis',
    3: 'football',
    4: 'baseball',
    5: 'basketball'
}

@app.route("/callsports/")
def main():
    """Respond to incoming requests."""
    resp = twilio.twiml.Response()
    if 'redirected' in session:
        resp.say("Main menu. Please select a sport.")
    else:
        session['redirected'] = True
        resp.say("Welcome to Call Sports. Please select a sport.")
    with resp.gather(numDigits=1, action='/callsports/sport', method='POST') as g:
        for num, sport in sports.items():
            g.say("For %s, press %s" % (sport, num))
    resp.say('Thanks for calling Call Sports, have a nice day!')
    
    return Response(str(resp), mimetype='text/xml')

@app.route("/callsports/sport", methods=["GET", "POST"])
def sport():
    """Respond to incoming requests."""
    pressed = request.values.get('Digits', None)
    sport = sports.get(int(pressed))
    message = ''
    resp = twilio.twiml.Response()
    headlines = []
    
    if pressed:
        resp.say("Welcome to news about %s" % sport)
        resp.pause(length=1)
        s_api = SportAPI(app.config['ESPN_API_KEY'])
        headlines = s_api.get_news(sport, 10)
    if not headlines:
        resp.say("No news about %" % sport)
        resp.pause(length=1)
    else:
        for headline in headlines:
            resp.say(headline)
            resp.play("%s/%s.mp3" % (app.config['MEDIA_ROOT_URL'], sport))
    resp.say('That is the end of the %s news' % sport)
    resp.redirect('/callsports')
    return Response(str(resp), mimetype='text/xml')

if __name__ == "__main__":
    app.run(debug=True)
