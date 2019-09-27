/**
 * @param {String} date
 * @returns {Object}
 */
module.exports = function (date) {
    return {
        date_obj: new Date(date),
        get value() {
            var year = this.date_obj.getFullYear();

            var month = parseInt(this.date_obj.getMonth()) + 1;
            month = this.addLeadingZero(month);

            var day = this.date_obj.getDate();
            day = this.addLeadingZero(day);

            var hour = this.date_obj.getHours();
            hour = this.addLeadingZero(hour);

            var minutes = parseInt(this.date_obj.getMinutes());
            minutes = this.addLeadingZero(minutes);

            return year + '-' + month + '-' + day + ' ' + hour + ':' + minutes;
        },
        addLeadingZero(timeValue) {
            if (timeValue < 10) {
                timeValue = '0' + timeValue
            }
            return timeValue;
        },
        add(amount, unit) {
            if (amount < 0) {
                throw new TypeError;
            };
            this.modifyObjDate(amount, unit, function(date_obj, amount){
                return date_obj + amount
            });
            return this;
        },
        subtract(amount, unit) {
            if (amount < 0) { 
                throw new TypeError('Incorrect amount');
            };
            this.modifyObjDate(amount, unit, function(date_obj, amount){
                return date_obj - amount
            });
            return this;
        },
        modifyObjDate(amount, unit, operation) {
            switch(unit) {
                case 'years':
                    this.date_obj.setFullYear(operation(this.date_obj.getFullYear(), amount));
                    break;
                case 'months':
                    this.date_obj.setMonth(operation(this.date_obj.getMonth(), amount));
                    break;
                case 'days':
                    this.date_obj.setDate(operation(this.date_obj.getDate(), amount));
                    break;
                case 'hours':
                    this.date_obj.setTime(operation(this.date_obj.getTime(), amount * 60 * 60 * 1000));
                    break;
                case 'minutes':
                    this.date_obj.setTime(operation(this.date_obj.getTime(), amount * 60 * 1000));
                    break;
                default: 
                    throw new TypeError('Incorrect time unit', unit);
            }
        }
    }
}
