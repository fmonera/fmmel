# fmmel
Software to control Mitsubishi Ecodan.

## Quickstart

### Run the image

This will launch a fmmel server at port 5000.

```
docker run -d --name fmmel --rm --publish 5000:5000 fmonera/fmmel:latest
```

### Get the token with your melcloud credentials

Open a browser and navigate to this URL:

```
http://localhost:5000/token?user=youruser@example.com&password=yourmelcloudpassword
```

You will get a response similar to: "FF6OZELCIZNADCEDZTIF"

Append the secret to any URL to interact with your installation.

### Update local data

You should not run this update more often than every few minutes.

Substitute with the secret you got when you logged in.

```
http://localhost:5000/update?secret=FF6OZELCIZNADCEDZTIF
```

### Get device info (after update)

```
http://localhost:5000/device?secret=FF6OZELCIZNADCEDZTIF
```

### Get zone info

```
http://localhost:5000/zone?secret=FF6OZELCIZNADCEDZTIF
```

### Set Hot Water Tank Temperature to 55C

```
http://localhost:5000/device/set/target_tank_temperature/55?secret=FF6OZELCIZNADCEDZTIF
```

### Set target heat flow temperature to 40C

```
http://localhost:5000/zone/set_target_heat_flow_temperature/40?secret=FF6OZELCIZNADCEDZTIF
```

