/**
 * Created by dheerenr on 6/7/15.
 */

if (!String.prototype.format) {
    String.prototype.format = function () {
        var args = arguments;
        return this.replace(/{(\d+)}/g, function (match, number) {
            return typeof args[number] != 'undefined'
                ? args[number]
                : match
                ;
        });
    };
}

if (!Date.prototype.getTwoDigitDate){
    Date.prototype.getTwoDigitDate = function(){
        return ("0" + this.getDate()).slice(-2);
    }
}

if (!Date.prototype.getTwoDigitMonth){
    Date.prototype.getTwoDigitMonth = function(){
        return ("0" + (this.getMonth() + 1)).slice(-2);
    }
}

if (!Date.prototype.getTwoDigitHour){
    Date.prototype.getTwoDigitHour = function(){
        return ("0" + this.getHours()).slice(-2);
    }
}

if (!Date.prototype.getTwoDigitMinute){
    Date.prototype.getTwoDigitMinute = function(){
        return ("0" + this.getMinutes()).slice(-2);
    }
}

if(!Date.prototype.iitbAppFormat){
    Date.prototype.iitbAppFormat = function(){
        var year = this.getFullYear();
        var month = this.getTwoDigitMonth();
        var day = this.getTwoDigitDate();
        var hour = this.getTwoDigitHour();
        var minutes = this.getTwoDigitMinute();

        return day + "-" + month + "-" + year + " " + hour + ":" + minutes;
    }
}