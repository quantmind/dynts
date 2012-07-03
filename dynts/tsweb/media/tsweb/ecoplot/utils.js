

(function($) {
    
    $.color_gradient = (function() {
        
        var hexDigits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"];
        
        // checks, if there is any unvalid digit for a hex number
        function checkHexDigits(s) {
            var j, found;
            for(var i = 0; i < s.length; i++) {
                found   = false;
                for(j = 0; j < hexDigits.length; j++)
                    if(s.substr(i, 1) == hexDigits[j])
                        found   = true;
                if(!found)
                    return false;
            }
            return true;
        }
        
        // checks, if a given number is a hexadezimal number
        function checkHex(hex) {
            if (!hex || hex==""  || hex=="#") throw "No valid hexadecimal given.";
            hex = hex.toUpperCase();            
            switch(hex.length) {
                case 6:
                    hex = "#" + hex;
                    break;
                case 7:
                    break;
                case 3:
                    hex = "#" + hex;
                    break;
                case 4:
                    hex = "#" + hex.substr(1, 1) + hex.substr(1, 1) + hex.substr(2, 1) + hex.substr(2, 1) + hex.substr(3, 1) + hex.substr(3, 1);
                    break;
            }
            if(hex.substr(0, 1) != "#" || !checkHexDigits(hex.substr(1))) {
                throw "No valid hexadecimal given.";
            }
            return hex; 
        }
        
        // generates a rgb value, using a hex value
        function hex2rgb(hex) {        
            var rgb = [];
            try {
                hex = checkHex(hex);
                rgb[0]=parseInt(hex.substr(1, 2), 16);
                rgb[1]=parseInt(hex.substr(3, 2), 16);
                rgb[2]=parseInt(hex.substr(5, 2), 16);
                return rgb;
            } catch (e) {
                throw e;
            }
        }

        //generates the hex-digits for a color. 
        function hex(x) {
            return isNaN(x) ? "00" : hexDigits[(x - x % 16) / 16] + hexDigits[x % 16];
        }
        
        // checks, if an array of three values is a valid rgb-array
        function checkRGB(rgb) {
             if (rgb.length!=3) throw "this is not a valid rgb-array";
             if (isNaN(rgb[0]) || isNaN(rgb[1]) || isNaN(rgb[2])) throw "this is not a valid rgb-array";
             if (rgb[0]<0 || rgb[0]>255 || rgb[1]<0 || rgb[1]>255 || rgb[2]<0 || rgb[3]>255) throw "this is not a valid rgb-array";
             return rgb;
        }
        
        // generates a hex value, using a rgb value
        function rgb2hex(rgb) {
            try {
                checkRGB(rgb);
                return "#" + hex(rgb[0]) + hex(rgb[1]) + hex(rgb[2]);
            } catch (e) {
                throw e;
            }
        }
        
        //compares two values to sort
        function cmp(a, b) {
            return a - b;
        }
        
        /**
         * calculateGradient for a color
         * @param startVal
         * @param endVal
         * @param count
         * @param type: array for each color. Speciefies, how the missing color should be calculated:
                                             1: linear
                                             2: trigonometrical 
                                             3: accidentally
                                             4: ordered accident
         */
         function calculateGradient(startVal, endVal, count, type) {
             var a = new Array();
             if(!type || !count) {
                 return null;
             } else if (1<count && count < 3) {
                 a[0] = startVal;
                 a[1] = endVal;
                 return a;
             } else if (count==1) {
                 a[0] = endVal;
                 return a;
             }
             
             switch(type) {
                 case 1: //"linear"
                     var i;
                     for(i = 0; i < count; i++)
                         a[i] = Math.round(startVal + (endVal - startVal) * i / (count - 1));
                     break;
         
                 case 2: //trigonometrical 
                     var i;
                     for(i = 0; i < count; i++)
                         a[i] = Math.round(startVal + (endVal - startVal) * ((Math.sin((-Math.PI / 2) + Math.PI * i / (count - 1)) + 1) / 2));
                     break;
         
                 case 3: //accident
                     var i;
                     for(i = 1; i < count - 1; i++)
                         a[i] = Math.round(startVal + (endVal - startVal) * Math.random());
                     a[0]    = startVal;
                     a[count - 1]    = endVal;
                     break;
         
                 case 4: //ordered accident
                     var i;
                     for(i = 1; i < count - 1; i++)
                         a[i] = Math.round(startVal + (endVal - startVal) * Math.random());
                     a[0]    = startVal;
                     a[count - 1]    = endVal;
                     if((typeof(a.sort) == "function") && (typeof(a.reverse) == "function"))
                     {
                         a.sort(cmp);
                         if(startVal > endVal)
                             a.reverse();
                     }
                     break;
             }
             return a;
         }
    
        /**
        * calculates an array with hex values. 
        * @param startColor: starting color (hex-format or rgb)
        * @param endColor: ending color (hex-format or rgb)
        * @param count: specifies, how many colors should be generated
        * @params types: array for each color.
        *         Speciefies, how the missing color should be calculated:
        *               1: linear
        *               2: trigonometrical 
        *               3: accidentally
        *               4: ordered accident
        */
        function calculateColor(startColor, endColor, count, types) {
            if(!types || types.length != 3) {
                types = [1,1,1];
            }
            var start,end,
                rgb = [],
                color = [];
            try {
                try {
                    start   = hex2rgb(startColor);
                    end     = hex2rgb(endColor);
                } catch (e) {
                    //no hex-value => check if rgb
                    checkRGB(startColor);
                    start = startColor;
                    checkRGB(endColor);
                    end = endColor;
                }
                
                rgb[0]  = calculateGradient(start[0], end[0], count, types[0]);
                rgb[1]  = calculateGradient(start[1], end[1], count, types[1]);
                rgb[2]  = calculateGradient(start[2], end[2], count, types[2]);
            
                for(var i = 0; i < count; i++) {
                    color[i] = "#" + hex(rgb[0][i]) + hex(rgb[1][i]) + hex(rgb[2][i]);
                }
            } catch (e) {
                throw e;
            }
            return color;
        }
        
        return calculateColor;
    }());
    
}(jQuery));
