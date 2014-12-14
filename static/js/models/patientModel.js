var app = app || {};

app.patientModel = Backbone.Model.extend({

	defaults: {
		/* DEMOGRAPHICS */
		name: "Patient Name",
		mrn: "12536212",
		age: "56",
		location: "6B 32-1",
}

});