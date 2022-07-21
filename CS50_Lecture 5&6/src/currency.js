// set endpoint and your access key
endpoint = 'latest'
access_key = 'NyzDGzX2Qs0MPTOYnekQAuM4sGT1yXlq';

// define from currency, to currency, and amount
var myHeaders = new Headers();
myHeaders.append("apikey", "BmEraBbsitLVcbqotXKeqji9PxWjVMEF");

var requestOptions = {
  method: 'GET',
  redirect: 'follow',
  headers: myHeaders
};

document.addEventListener('DOMContentLoaded', function(){

    document.querySelector('form').onsubmit = function() {

        fetch("https://api.apilayer.com/exchangerates_data/latest?base=USD", requestOptions)
        .then(response => response.json())
        .then(result => {
            const currency = document.querySelector('#currency').value.toUpperCase();
            const data = result.rates[currency];
            if (data !== undefined){
                document.querySelector('#result').innerHTML = `1 USD is equal to ${data.toFixed(3)} ${currency} now.`;
            } else{
                document.querySelector('#result').innerHTML = 'Invalid currency.';
            }

            })
        .catch(error => console.log('error', error));
        
        return false;
    }

});