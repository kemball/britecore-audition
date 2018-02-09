 var risk_list = new Vue({
        el: '#list_of_risks',
        data: {
          risks:[]
        },
        mounted: function(){
        	var self= this;
        	fetch(url_risks)
        	.then(function(response){
        		var my_json = response.json();
        		console.log(my_json);
        		return my_json;
        	})
        	.then(function(json){

        		self.risks = json;
        		return json;
        	})
        }

      })


