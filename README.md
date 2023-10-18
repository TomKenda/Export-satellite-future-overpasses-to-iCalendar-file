# Export satellite's future overpasses to iCalendar file
@authors : Tom Kenda (UCLouvain), Octobre 2023, PHENET Project

This script is used to get the date and time when Sentinels will fly over a given zone.
After this, an .ics file is created to be imported in a calendar application (e.g. Google Calendar)

For more info see : 
* https://api.spectator.earth/?language=Python#spectator-api-docs and
* https://icspy.readthedocs.io/en/stable/api.html#calendar

Available satellites are :

Sentinel-1A, Sentinel-1B, Sentinel-2A, Sentinel-2B, Sentinel-3A, Landsat-8
