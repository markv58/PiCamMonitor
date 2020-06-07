/* Magic Mirror Config Sample
 *
 * By Michael Teeuw http://michaelteeuw.nl
 * MIT Licensed.
 *
 * For more information how you can configurate this file
 * See https://github.com/MichMich/MagicMirror#configuration
 *
 */

var config = {
        address: "localhost", // Address to listen on, can be:
                              // - "localhost", "127.0.0.1", "::1" to listen on loopback interface
                              // - another specific IPv4/6 to listen on a specific interface
                              // - "", "0.0.0.0", "::" to listen on any interface
                              // Default, when address config is left out, is "localhost"
        port: 8080,
        ipWhitelist: [], // Set [] to allow all IP addresses
                                                               // or add a specific IPv4 of 192.168.1.5 :
                                                               // ["127.0.0.1", "::ffff:127.0.0.1", "::1", "::ffff:192.168.1.5"],
                                                               // or IPv4 range of 192.168.3.0 --> 192.168.3.15 use CIDR format :
                                                               // ["127.0.0.1", "::ffff:127.0.0.1", "::1", "::ffff:192.168.3.0/28"],

        language: "en",
        timeFormat: 12,
        units: "imperial",

        modules: [
                {
                        module: "clock",
                        position: "top_left"
                },
                {
                        module: "currentweather",
                        position: "bottom_left",
                        config: {
                                location: "Richardson", //Your city here <<
                                locationID: "4722625",  //ID from http://bulk.openweathermap.org/sample/; unzip the gz file and find your city
                                appid: "yourAPIkeygoeshere",  //API key <<<
                                showHumidity: "true",
                                roundTemp: "true",
                                units: "imperial",
                                updateInterval: "1800000"
                        }
                },
                {
                        module: "weatherforecast",
                        position: "bottom_right",
                        header: "Weather Forecast",
                        config: {
                                location: "Richardson",  //Your city here <<
                                locationID: "4722625",  //ID from https://openweathermap.org/city
                                appid: "yourAPIkeygoeshere",  //API key <<<
                                roundTemp: "true",
                                updateInterval: "3000000",
                                initialLoadDelay: "2500"
                        }
                },
                {
                        module: "MMM-BackgroundSlideshow",
                        position: "fullscreen_below",
                        config: {
                                imagePaths: ["modules/Pictures/"],
                                backgroundSize: "contain",
                                transitionImages: "true",
                                transitionSpeed: "1s",
                                slideshowSpeed: "30000",
                                gradientDirection: "horizontal"
                        }
                },
        ]

};

/*************** DO NOT EDIT THE LINE BELOW ***************/
if (typeof module !== "undefined") {module.exports = config;}
