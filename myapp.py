from flask import Flask, jsonify, json, request
all_records = [
        {
                "name" : "Radiohead",
                "albums" : [
                        {
                                "title":"The King of Limbs",
                                "songs":["..."],
                                "description":"..."
                        },
                        {
                                "title":"OK Computer",
                                "songs":[],
                                "description":"..."
                        }
                        ]
                        },
        {
                "name":"Portishead",
                "albums":[
                        {
                                "title":"Dummy",
                                "songs":[],
                                "description":"..."
                        },
                        {
                                "title":"Third",
                                "songs":[],
                                "description":"..."
                        }
                        ]
        }
]

app = Flask(__name__)


@app.route('/')
def hello():
	return "<h1>Hello, World!</h1>"

@app.route('/records/', methods=['GET'])
def get_records():
	return jsonify(all_records)

@app.route('/records/all_bands/', methods=['GET'])
def get_bands():
	response = [item['name'] for item in all_records]
	return jsonify(response)

@app.route('/records/albums_by_band/<bandname>/', methods=['GET'])
def get_album_by_band(bandname):
	response={bandname:'Not Found!'}
	for item in all_records:
		if item["name"]==bandname:
			response = [x["title"] for x in item["albums"]]
			break
	return jsonify(response)

@app.route('/records', methods=['POST'])
def create_a_record():
	if not request.json or not 'name' in request.json:
		return jsonify({'error':'the new record needs to have a band name'}), 400
	new_record = {
	'name': request.json['name'],
	'albums': request.json.get('albums', '')
	}
	all_records.append(new_record)
	return jsonify({'message': 'created: /records/{}'.format(new_record['name'])}), 20

@app.route('/records/<bandname>', methods=['DELETE'])
def delete_a_band(bandname):
	matching_records = [band for band in all_records if band['name'] == bandname]
	if len(matching_records)==0:
		return jsonify({'error':'band name not found!'}), 404
	all_records.remove(matching_records[0])
	return jsonify({'success': True})

@app.route('/records/<bandname>/<album>/<song>', methods=['DELETE'])
def delete_song(bandname, album, song):
    matching_band = next((band for band in all_records if band['name'] == bandname), None)

    if not matching_band:
        return jsonify({'error': 'Band name not found!'}), 404

    matching_album = next((a for a in matching_band['albums'] if a['title'] == album), None)

    if not matching_album:
        return jsonify({'error': 'Album not found!'}), 404

    if song in matching_album['songs']:
        matching_album['songs'].remove(song)
        return jsonify({'success': True, 'message': f"Song '{song}' removed from '{album}' by '{bandname}'"})
    else:
        return jsonify({'error': 'Song not found in the album'}), 404

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)
