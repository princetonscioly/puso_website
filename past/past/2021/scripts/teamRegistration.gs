var formID = '';
var SENDGRID_KEY = '';

var totalTeamCountLimit = 4;
var secondTeamCountLimit = 1;

var pusoDate = 'February 8th, 2020';
var withdrawDate = '11:59 PM EST November 22, 2019';
var pusoEmail = 'scioly@princeton.edu';

var FIELDS = {
  'coachFirstName': 0,
  'coachLastName': 1,
  'coachEmail': 2,
  'coachPhoneNumber': 3,
  'teamCaptainEmail': 4,
  'schoolName': 5,
  'schoolStreetAddress': 6,
  'city': 7,
  'state': 8,
  'zipCode': 9,
  'schoolPrincipalFirstName': 10,
  'schoolPrincipalLastName': 11,
  'teamsToRegister': 12,
  'agreement': 13,
};

function initializeProperties(){
  PropertiesService.getScriptProperties().setProperty('totalTeamCount', 0);
  PropertiesService.getScriptProperties().setProperty('secondTeamCount', 0);
}

function openForm(){
  var form = FormApp.openById(formID);
  form.setAcceptingResponses(true);
}

function closeForm(){
  var form = FormApp.openById(formID);
  form.setAcceptingResponses(false);
}

function onSubmit(e){
  var itemResponses = e.response.getItemResponses();
  var numTeams = Number(itemResponses[FIELDS.teamsToRegister].getResponse());
  
  var totalTeamCount = Number(PropertiesService.getScriptProperties().getProperty('totalTeamCount'));
  var secondTeamCount = Number(PropertiesService.getScriptProperties().getProperty('secondTeamCount'));
  
  var acceptAll = false;
  var acceptOne = false;
  
  if (totalTeamCount < totalTeamCountLimit) {          // Check if there's any space remaining
    totalTeamCount += 1;
    if (numTeams == 1) {
      acceptAll = true;
    } else if (numTeams == 2) {
      if (secondTeamCount < secondTeamCountLimit) {    // Check if there's space for a second team
        totalTeamCount += 1;
        secondTeamCount += 1;
        acceptAll = true;
      } else {
        acceptOne = true;
      }
    } else {
      Logger.log('Invalid input: ' + numTeams);
    }
  
    PropertiesService.getScriptProperties().setProperty('totalTeamCount', totalTeamCount);
    PropertiesService.getScriptProperties().setProperty('secondTeamCount', secondTeamCount);
  }
  
  sendConfirmation(itemResponses, acceptAll, acceptOne);
}

function test() {
  Logger.log(Utilities.formatString('hi %s %d', 'there', secondTeamCountLimit)); 
}

function sendConfirmation(responses, all, one) {
  var coachFirstName = responses[FIELDS.coachFirstName].getResponse();
  var coachLastName = responses[FIELDS.coachLastName].getResponse();
  var coachEmail = responses[FIELDS.coachEmail].getResponse();
  var teamCaptainEmail = responses[FIELDS.teamCaptainEmail].getResponse();
  var schoolName = responses[FIELDS.schoolName].getResponse();
  var numTeams = Number(responses[FIELDS.teamsToRegister].getResponse());
  var plural = numTeams == 1 ? '' : 's';
  
  var bodyGreeting = Utilities.formatString('Hi %s %s,', coachFirstName, coachLastName);
  
  var body1 = all ? Utilities.formatString('%s has successfully registered %d team%s for the Princeton University Science Olympiad Invitational on %s!', schoolName, numTeams, plural, pusoDate)
            : one ? Utilities.formatString('%s has successfully registered 1 team for the Princeton University Science Olympiad Invitational on %s! Due to our cap of %d schools with two teams, we are unfortunately unable to register your second team at this time. If spots open in the future, we will contact you with the opportunity to register your other team.', schoolName, pusoDate, secondTeamCountLimit)
                  : Utilities.formatString('Due to our cap of %d teams, %s has been placed on the waitlist for the Princeton University Science Olympiad Invitational on %s.', totalTeamCountLimit, schoolName, pusoDate);
  
  var body2 = all || one ? Utilities.formatString('Please keep this email as your registration confirmation. Should you choose to withdraw your team%s from our tournament after %s, your school will incur a $100 fee per team withdrawn. Please reply to this email to acknowledge that you have received this email, understand the terms of your registration, and intend to participate in the tournament.', plural, withdrawDate)
                         : 'Please reply to this email to acknowledge that you would like to remain on the waitlist, and we will contact you if a spot opens up.';

  var body3 = all || one ? Utilities.formatString('We are excited to welcome you to Princeton and we look forward to seeing you at our tournament! If you have any questions, please contact us at %s. Required waiver forms and team rosters will be sent out in a few months.', pusoEmail)
                         : Utilities.formatString('We hope to welcome you to Princeton! If you have any questions, please contact us at %s.', pusoEmail);
  
  var signature = 'Sincerely,\n\nNicole Meister and Andy Xu\nCo-Directors';
  var bodyContent = Utilities.formatString('%s\n\n%s\n\n%s\n\n%s\n\n%s', bodyGreeting, body1, body2, body3, signature); 
  
  Logger.log(bodyContent);
  
  sendEmail(coachFirstName, coachLastName, coachEmail, teamCaptainEmail, bodyContent);
}

function sendEmail(coachFirstName, coachLastName, coachEmail,teamCaptainEmail, bodyContent){
  var headers = {
    "Authorization" : "Bearer " + SENDGRID_KEY, 
    "Content-Type": "application/json" 
  };
  
  var body = {
    "personalizations": [{
      "to": [ { 
        "name": Utilities.formatString('%s %s', coachFirstName, coachLastName),
        "email": coachEmail,
      } ],
      "bcc" : [ { "email": pusoEmail } ],
      "subject": "Thank You for Registering for the 2020 Princeton University Science Olympiad Invitational!"
    }],
    
    "from": {
      "name": "Princeton University Science Olympiad",
      "email": pusoEmail,
    },
    
    "content": [{
      "type": "text",
      "value": bodyContent
    }]
  };
  
  if (teamCaptainEmail) {
    body["personalizations"]["cc"] = teamCaptainEmail
  }

  var options = {
    'method': 'POST',
    'headers': headers,
    'payload': JSON.stringify(body)
  };

  var response = UrlFetchApp.fetch("https://api.sendgrid.com/v3/mail/send", options);

  Logger.log(response); 
}
