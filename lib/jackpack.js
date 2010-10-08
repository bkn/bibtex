
function formattedJSON(jobj,output_to) {
	var result_str = "";
	if(output_to == "file"){					
		result_str = JSON.stringify(jobj, null, '\t');
		result_str = result_str.replace(/\t/g, "  ");
		result_str = result_str.replace(/\n/g, "\n");
	}
	else {
		result_str = JSON.stringify(jobj, null, '\t');
		result_str = result_str.replace(/\t/g, "&nbsp;&nbsp;");
		result_str = result_str.replace(/\n/g, "<br>");				
	}
	return result_str;					
}


function deb(str, linebreak){
	
	var debug_id = document.getElementsByTagName("BODY").item(0);
	if (document.getElementById('debug_area')) {
		debug_id = document.getElementById('debug_area');
	}
	if (linebreak == undefined){
	    $(debug_id).append("<br>");        
	}
	$(debug_id).append(str);  
}


var Utf8 = {
 
	// public method for url encoding
	encode : function (string) {
		string = string.replace(/\r\n/g,"\n");
		var utftext = "";
 
		for (var n = 0; n < string.length; n++) {
 
			var c = string.charCodeAt(n);
 
			if (c < 128) {
				utftext += String.fromCharCode(c);
			}
			else if((c > 127) && (c < 2048)) {
				utftext += String.fromCharCode((c >> 6) | 192);
				utftext += String.fromCharCode((c & 63) | 128);
			}
			else {
				utftext += String.fromCharCode((c >> 12) | 224);
				utftext += String.fromCharCode(((c >> 6) & 63) | 128);
				utftext += String.fromCharCode((c & 63) | 128);
			}
 
		}
 
		return utftext;
	},
 
	// public method for url decoding
	decode : function (utftext) {
		var string = "";
		var i = 0;
		var c = c1 = c2 = 0;
 
		while ( i < utftext.length ) {
 
			c = utftext.charCodeAt(i);
 
			if (c < 128) {
				string += String.fromCharCode(c);
				i++;
			}
			else if((c > 191) && (c < 224)) {
				c2 = utftext.charCodeAt(i+1);
				string += String.fromCharCode(((c & 31) << 6) | (c2 & 63));
				i += 2;
			}
			else {
				c2 = utftext.charCodeAt(i+1);
				c3 = utftext.charCodeAt(i+2);
				string += String.fromCharCode(((c & 15) << 12) | ((c2 & 63) << 6) | (c3 & 63));
				i += 3;
			}
 
		}
 
		return string;
	}
 
}

function is_url (str, k, obj) {
	
	// search for http
	// if found extract http:// to [non-url char]
	// elseif search for www
 	// if found extract http:// to [non-url char]

	// if url found split str
	//  
	//	use preceding str as label if separated by space, 
	//  
	//  or use obj['prefLabel'] ?
	//  or use key name if not contain 'url'?
	//  or use following value between > </a> (beware of \>, \<, \/)
	//  or use domain name value between http:// or www. and first / 	
	
	v = $.trim(str)
	url = null;
	http_pattern = /http\:\/\/.*/gi;
	www_pattern = /www\.*/gi;
	url_list = v.match(http_pattern); 	
	
	// 	NOT YET HANDLING LIST OF URLS
	
	if (url_list) {
		// match finds the first occurence of a url to the end of string
		// some strings are space separated lists, and have multiple urls
		// so we get the first match and need to split at the first space
		url = url_list[0].split(' ')[0]; 

	}
	else {
		url_list = v.match(www_pattern)	;
		if (url_list) {
		url = url_list[0].split(' ')[0]; // some strings are space separated lists
		}
	} 
	return url;
}

function make_link(url, title){
	return "<a href=\'" + url + "'>" + title + "</a>"
}

function extract_domain_name(url) {
	var domain_name = url.replace('http://','');
	domain_name = domain_name.replace('www.','');
	var end = domain_name.indexOf('/'); 
	if (end == -1) {
		domain_name = domain_name.substring(0)		
	}
	else {
		domain_name = domain_name.substring(0,end)		
	}	
	return domain_name;
}