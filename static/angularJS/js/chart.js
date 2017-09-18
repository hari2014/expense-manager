

  google.load('visualization', '1', {packages:['corechart']});
google.setOnLoadCallback(function() {
  angular.bootstrap(document.body, ['project']);
});

angular.module('project').controller('pichart', function($scope,$http) {
    console.log("Hello");
         $http.get("/data")
    .then(function(response) {
        $scope.jsonData = response.data;
    });

    console.log($scope.jsonData)


        var data = new google.visualization.DataTable();
      data.addColumn('string', 'Category');
        data.addColumn('number', 'Amount');

        data.addRows(JSON.parse($scope.jsonData));


      var chart = new google.visualization.PieChart(document.getElementById('pie'));
      chart.draw(data, {width: 600, height: 500});
    }
  );