
    # Insert placemarks for each stop. Track the altitude in case some lines are missing it.
    last_alt 	= 0
    for stop in stops.values():
        if 'altitude' in stop:
            last_alt 	= stop['altitude']

        kml_file.write('<Placemark>\n')
        kml_file.write('\t<description>Red PIN for A Stop</description>\n')
        kml_file.write('\t<Style>\n')
        kml_file.write('\t\t<IconStyle>\n')
        kml_file.write('\t\t\t<color>ff0000ff</color>\n')
        kml_file.write('\t\t\t<Icon>\n')
        kml_file.write('\t\t\t\t<href>http://maps.google.com/mapfiles/kml/paddle/1.png</href>\n')
        kml_file.write('\t\t\t</Icon>\n')
        kml_file.write('\t\t</IconStyle>\n')
        kml_file.write('\t</Style>\n')
        kml_file.write('\t<Point>\n')
        kml_file.write(
            '\t\t<coordinates>' + str(stop['longitude']) + ',' + str(stop['latitude']) + ',' + str(last_alt) +
            '</coordinates>\n')
        kml_file.write('\t</Point>\n')
        kml_file.write('</Placemark>\n')

    # Insert placemarks for each left turn. Track the altitude in case some lines are missing it.
    for left in left_turns.values():
        if 'altitude' in left:
            last_alt 	= left['altitude']

        kml_file.write('<Placemark>\n')
        kml_file.write('\t<description>Yellow PIN for a Left</description>\n')
        kml_file.write('\t<Style>\n')
        kml_file.write('\t\t<IconStyle>\n')
        kml_file.write('\t\t\t<color>ff00ffff</color>\n')
        kml_file.write('\t\t\t<Icon>\n')
        kml_file.write('\t\t\t\t<href>http://maps.google.com/mapfiles/kml/paddle/1.png</href>\n')
        kml_file.write('\t\t\t</Icon>\n')
        kml_file.write('\t\t</IconStyle>\n')
        kml_file.write('\t</Style>\n')
        kml_file.write('\t<Point>\n')
        kml_file.write(
            '\t\t<coordinates>' + str(left['longitude']) + ',' + str(left['latitude']) + ',' + str(last_alt) +
            '</coordinates>\n')
        kml_file.write('\t</Point>\n')
        kml_file.write('</Placemark>\n')

    # Insert placemarks for each right turn. Track the altitude in case some lines are missing it.
    for right in right_turns.values():
        if 'altitude' in right:
            last_alt 	= right['altitude']

        kml_file.write('<Placemark>\n')
        kml_file.write('\t<description>Cyan PIN for A Right</description>\n')
        kml_file.write('\t<Style>\n')
        kml_file.write('\t\t<IconStyle>\n')
        kml_file.write('\t\t\t<color>ffffff00</color>\n')
        kml_file.write('\t\t\t<Icon>\n')
        kml_file.write('\t\t\t\t<href>http://maps.google.com/mapfiles/kml/paddle/1.png</href>\n')
        kml_file.write('\t\t\t</Icon>\n')
        kml_file.write('\t\t</IconStyle>\n')
        kml_file.write('\t</Style>\n')
        kml_file.write('\t<Point>\n')
        kml_file.write(
            '\t\t<coordinates>' + str(right['longitude']) + ',' + str(right['latitude']) + ',' + str(last_alt) +
            '</coordinates>\n')
        kml_file.write('\t</Point>\n')
        kml_file.write('</Placemark>\n')

