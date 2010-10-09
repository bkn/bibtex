
function status (message) {
	$('#status').html(message);
}

function show_json(response){

	deb(formattedJSON(response));
// add test to display if result is text
	//	deb("RESPONSE as text: " + response);

}

function get_user_input() {
	var params = '';
	var user_input = '';
	user_input = $('#bibtex_data').val();
	params = '&document='+encodeURIComponent(user_input);
	if (!user_input) {
		user_input = $('#bibtex_url').val();
		params = '&url='+encodeURIComponent(user_input);
	}
	return params;
}

function get_attributes(response) {
	var facets = {}
	for (var i=0; i < response.length; i++) {
		for(var r in response[i]) {
			if (r in facets) {
				facets[r]++;				
			}
			else {
				facets[r] = 1;
			}
		}
	}
	return facets;
}

function show_csv(response) {
	var facets = get_attributes(response);
	var headers = [];
	var i = 0;
	var x = 0;
	var k;
	var content = '';
	for (k in facets) {
		headers[i] = k;
		i++;
	}
	for (x=0; x < headers.length; x++) {
		if (x != 0) {
			content += ',';
		}
		content += headers[x];
	}
	content += '\n';
	
	for (i=0; i < response.length; i++) {
		for (x=0; x < headers.length; x++) {
			if (x != 0) {
				content += ',';
			}
			k = headers[x];
			if ((k in response[i]) && response[i][k]) {
				content += '"'+response[i][k]+'"';				
			}
		}
		content += '\n';
	}	
	$('#csv_data').html(content);
}

function show_csv_area() {
	var content = '';
	$('#csv_area').html("");
	$('#csv_area').append("<div class='block_header'>CSV Document</div>");
	content = "<form><div id='csv_form' class='csv_form'></div></form>"; 	
	$('#csv_area').append(content);
//	content = "<form>Show as: ";
//	content += "  <input type='button' value='Table' id='csv_table_button' class='_button'/>";
//	content += "  <input type='button' value='Text' id='csv_text_button' class='_button'/>";
//	content += "</form>";
//	$('#csv_form').html(content);
	content = '<textarea id="csv_data" class="csv_data" type="textarea" value=""> </textarea>';
	$('#csv_form').append(content);
}

function show_bibjson(response) {
	$('#json_data').html(formattedJSON(response,'file'));
}

function show_conversion(response) {
	show_bibjson(response);
	show_csv(response);
}

function show_bibtex_area() {
	var content = '';
	$('#bibtex_area').html("");
	$('#bibtex_area').append("<div class='block_header'>BibTeX Document</div>");
	content = "<form><div id='bibtex_form' class='bibtex_form'></div></form>"; 	
	$('#bibtex_area').append(content);
	
	content = "<form>Convert to: ";
	content += "  <input type='button' value='Convert' id='convert_button' class='_button'/>";
//	content += "  <input type='button' value='JSON' id='bibtex_json_button' class='_button'/>";
//	content += "  <input type='button' value='CSV' id='bibtex_csv_button' class='_button'/>";
	content += "</form>";
	$('#bibtex_form').append(content);
	
	content = '<div>Enter a URL:</div>';	
	content += '<div><input id="bibtex_url" class="bibtex_url" type="text" value="" /></div>';	
	$('#bibtex_form').append(content);
	
	content = '<div> or add text below:</div>';
	content += '<div><textarea id="bibtex_data" class="bibtex_data" value=""';
	content += 'spellcheck="true"';
	content += '></textarea></div>';
	$('#bibtex_form').append(content);

	$('#convert_button').click(function () {
		$('#csv_data').html('');
		$('#json_data').html('');

		bibtex_service(show_conversion,get_user_input());
		});			
//	$('#bibtex_json_button').click(function () {
//		bibtex_service(show_bibjson,get_user_input());
//		});			
//	$('#bibtex_csv_button').click(function () {
//		bibtex_service(show_csv,get_user_input());
//		});			

}

function show_json_area() {
	var content = '';
	$('#json_area').html("");
	$('#json_area').append("<div class='block_header'>JSON Document</div>");
	content = "<form><div id='json_form' class='json_form'></div></form>"; 
	$('#json_area').append(content);
	content = '<textarea id="json_data" class="json_data" type="textarea" value=""> </textarea>';
	$('#json_form').append(content);
//	content = "<form><input type='button' value='Convert' id='convert_button' class='_button'/></form>";
//	$('#json_form').append(content);
//	$('#json_button').click(function () {
//		var params = '&document='+encodeURIComponent($('#json_form').val());
//		bibtex_service(show_bibtex,params);
//		});			
}


function show_template_page () {
	var content = '';
	
	$('body').append("<div id='page_header_wrapper' class='page_header_wrapper'></div>");
	$('body').append("<div id='info_area' class='info_area'></div>");
	$('body').append("<div id='bibtex_area' class='bibtex_area'></div>");
	$('body').append("<div id='json_area' class='json_area'></div>");
	$('body').append("<div id='csv_area' class='csv_area'></div>");
	
	$('#page_header_wrapper').html("<div class='logo'>BKN BibTex / JSON Converter</div>");
	content = "<div class='page_subheader'>";
	content += "Brought to you by Bibliographic Knowledge Network<br>DEVELOPMENT TEST VERSION"; 
	content += "</div>";
	$('#page_header_wrapper').append(content);

	$('#info_area').append("<div id='active_info' class='info_active'></div>");

	$('#active_info').append("<div id='status' class='status'></div>");
	show_bibtex_area();
	show_json_area();
	show_csv_area();
	
}


function bibtex_service(callback, service_params) {
	var script = "cgi-bin/bibtex/bibtex.py";
	var location = "http://" + window.location.hostname + "/";
	var service = "" + location + script;
//deb(service +"?"+service_params);
    $.ajax({
        url: service,
        data: service_params,
        type: "post",
        cache: false,
        dataType: "jsonp",
        error: function(xobj, status, error){
			    	show_json({'xobj':xobj, 'status':status,'error':error});
			        },
        success: function (response) {
		        	if (response && ('error' in response)) {
		        		show_json(response);
		        	}
		        	else {
	        			callback(response);		        		
		        	}
		      	}
    }); 
}

var bibtex_str = '';
bibtex_str += '@article{bleij06, ';
bibtex_str += '	author = {D. Blei and M. Jordan},';
bibtex_str += ' title =        {Variational inference for {D}irichlet process mixtures},';
bibtex_str += ' journal =      {Journal of Bayesian Analysis},';
bibtex_str += ' year =         {2006},';
bibtex_str += ' volume =       {1},';
bibtex_str += ' pages =        {121-144},';
bibtex_str += '}'	;

var params = '';
//params += '&file=yor.bib';
//params += '&url=http://localhost/bkn/bibtex/temp.bib';	
params += '&document='+encodeURIComponent(bibtex_str);
	
//bibtex_service(show_json,params);
show_template_page();