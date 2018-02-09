

Vue.component("risk_field",{
	template: `
	<div class="stack_horizontal">
		<span class="label">{{f_name}}</span><br>
		<input  :name='f_name' :type='f_type'>
	</div>
	`,
	props:['f_name','f_type']

})

Vue.component("risk-viewer",{
  	template : `
  	<div v-on:click='expand'>
  		{{risk_name}} <br> 
  		<div v-if='expanded'>
  			<form>
  			<div class="r_f" v-for="field in fields">
  				<risk_field :f_name="field.name" :f_type="field.type"></risk_field>
  			</div>
  			<input type="submit" value="add new entry">
  			</form>
  		</div>
  		<div v-else>
  			<button>expand</button>
  		</div>
  	</div>
  	`,
	props:['risk_name'],
	data :function(){
		return {
			expanded: false,
			fields: []}
	},
	methods:{
		expand: function(){
			console.log("expanding " + this.risk_name);
			this.expanded=true;
			var self=this;
			fetch(url_risk+this.risk_name)
			.then(function(response){
				return response.json()
			})
			.then(function(json){
				self.risk_name = json.name
				self.fields=json.fields
			})
		}
	}
})