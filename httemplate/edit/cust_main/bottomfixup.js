<%init>
my %opt = @_; # custnum
my $conf = new FS::Conf;

my $company_latitude  = $conf->config('company_latitude');
my $company_longitude = $conf->config('company_longitude');

my @fixups = ('copy_payby_fields', 'standardize_locations');

push @fixups, 'fetch_censustract'
    if $conf->exists('cust_main-require_censustract');

push @fixups, 'check_unique'
    if $conf->exists('cust_main-check_unique') and !$opt{'custnum'};

push @fixups, 'do_submit'; # always last
</%init>

var fixups = <% encode_json(\@fixups) %>;
var fixup_position;

%# state machine to deal with all the asynchronous stuff we're doing
%# call this after each fixup on success:
function submit_continue() {
  window[ fixups[fixup_position++] ].call();
}

%# or on failure:
function submit_abort() {
  fixup_position = 0;
  document.CustomerForm.submitButton.disabled = false;
  cClick();
}

function bottomfixup(what) {
  fixup_position = 0;
  document.CustomerForm.submitButton.disabled = true;
  submit_continue();
}

function do_submit() {
  document.CustomerForm.submit();
}

function copy_payby_fields() {
  var layervars = new Array(
    'payauto', 'billday',
    'payinfo', 'payinfo1', 'payinfo2', 'payinfo3', 'paytype',
    'payname', 'paystate', 'exp_month', 'exp_year', 'paycvv',
    'paystart_month', 'paystart_year', 'payissue',
    'payip',
    'paid'
  );

  var cf = document.CustomerForm;
  var payby = cf.payby.options[cf.payby.selectedIndex].value;
  for ( f=0; f < layervars.length; f++ ) {
    var field = layervars[f];
    copyelement( cf.elements[payby + '_' + field],
                 cf.elements[field]
               );
  }
  submit_continue();
}

%# call submit_continue() on completion...
%# otherwise not touching standardize_locations for now
<% include( '/elements/standardize_locations.js',
            'callback' => 'submit_continue();',
            'main_prefix' => 'bill_',
            'no_company' => 1,
          )
%>

var prefix;
function fetch_censustract() {

  //alert('fetch census tract data');
  prefix = document.getElementById('same').checked ? 'bill_' : 'ship_';
  var cf = document.CustomerForm;
  var state_el = cf.elements[prefix + 'state'];
  var census_data = new Array(
    'year',     <% $conf->config('census_year') || '2012' %>,
    'address1', cf.elements[prefix + 'address1'].value,
    'city',     cf.elements[prefix + 'city'].value,
    'state',    state_el.options[ state_el.selectedIndex ].value,
    'zip',      cf.elements[prefix + 'zip'].value
  );

  censustract( census_data, update_censustract );

}

var set_censustract;

function update_censustract(arg) {

  var argsHash = eval('(' + arg + ')');

  var cf = document.CustomerForm;

/*  var msacode    = argsHash['msacode'];
  var statecode  = argsHash['statecode'];
  var countycode = argsHash['countycode'];
  var tractcode  = argsHash['tractcode'];
  
  var newcensus = 
    new String(statecode)  +
    new String(countycode) +
    new String(tractcode).replace(/\s$/, '');  // JSON 1 workaround */
  var error      = argsHash['error'];
  var newcensus  = argsHash['censustract'];

  set_censustract = function () {

    cf.elements[prefix + 'censustract'].value = newcensus;
    submit_continue();

  }

  if (error || cf.elements[prefix + 'censustract'].value != newcensus) {
    // popup an entry dialog

    if (error) { newcensus = error; }
    newcensus.replace(/.*ndefined.*/, 'Not found');

    var latitude = cf.elements[prefix + 'latitude'].value 
                   || '<% $company_latitude %>';
    var longitude= cf.elements[prefix + 'longitude'].value 
                   || '<% $company_longitude %>';

    var choose_censustract =
      '<CENTER><BR><B>Confirm censustract</B><BR>' +
      '<A href="http://maps.ffiec.gov/FFIECMapper/TGMapSrv.aspx?' +
      'census_year=<% $conf->config('census_year') || '2012' %>' +
      '&latitude=' + latitude +
      '&longitude=' + longitude +
      '" target="_blank">Map service module location</A><BR>' +
      '<A href="http://maps.ffiec.gov/FFIECMapper/TGMapSrv.aspx?' +
      'census_year=<% $conf->config('census_year') || '2012' %>' +
      '&zip_code=' + cf.elements[prefix + 'zip'].value +
      '" target="_blank">Map zip code center</A><BR><BR>' +
      '<TABLE>';
    
    choose_censustract = choose_censustract + 
      '<TR><TH style="width:50%">Entered census tract</TH>' +
        '<TH style="width:50%">Calculated census tract</TH></TR>' +
      '<TR><TD>' + cf.elements[prefix + 'censustract'].value +
        '</TD><TD>' + newcensus + '</TD></TR>' +
        '<TR><TD>&nbsp;</TD><TD>&nbsp;</TD></TR>';

    choose_censustract = choose_censustract +
      '<TR><TD ALIGN="center">' +
        '<BUTTON TYPE="button" onClick="submit_continue();"><IMG SRC="<%$p%>images/error.png" ALT=""> Use entered census tract </BUTTON>' + 
      '</TD><TD ALIGN="center">' +
        '<BUTTON TYPE="button" onClick="set_censustract();"><IMG SRC="<%$p%>images/tick.png" ALT=""> Use calculated census tract </BUTTON>' + 
      '</TD></TR>' +
      '<TR><TD COLSPAN=2 ALIGN="center">' +
        '<BUTTON TYPE="button" onClick="submit_abort();"><IMG SRC="<%$p%>images/cross.png" ALT=""> Cancel submission</BUTTON></TD></TR>' +
        
      '</TABLE></CENTER>';

    overlib( choose_censustract, CAPTION, 'Confirm censustract', STICKY, AUTOSTATUSCAP, CLOSETEXT, '', MIDX, 0, MIDY, 0, DRAGGABLE, WIDTH, 576, HEIGHT, 268, BGCOLOR, '#333399', CGCOLOR, '#333399', TEXTSIZE, 3 );

  } else {

    submit_continue();

  }

}

function copyelement(from, to) {
  if ( from == undefined ) {
    to.value = '';
  } else if ( from.type == 'select-one' ) {
    to.value = from.options[from.selectedIndex].value;
    //alert(from + " (" + from.type + "): " + to.name + " => (" + from.selectedIndex + ") " + to.value);
  } else if ( from.type == 'checkbox' ) {
    if ( from.checked ) {
      to.value = from.value;
    } else {
      to.value = '';
    }
  } else {
    if ( from.value == undefined ) {
      to.value = '';
    } else {
      to.value = from.value;
    }
  }
  //alert(from + " (" + from.type + "): " + to.name + " => " + to.value);
}

function check_unique() {
  var search_hash = new Object;
% foreach ($conf->config('cust_main-check_unique')) {
  search_hash['<% $_ %>'] = document.CustomerForm.elements['<% $_ %>'].value;
% }

%# supported in IE8+, Firefox 3.5+, WebKit, Opera 10.5+
  duplicates_form(JSON.stringify(search_hash), confirm_unique);
}

function confirm_unique(arg) {
  if ( arg.match(/\S/) ) {
%# arg contains a complete form to choose an existing customer, or not
  overlib( arg, CAPTION, 'Duplicate customer', STICKY, AUTOSTATUSCAP, 
      CLOSETEXT, '', MIDX, 0, MIDY, 0, DRAGGABLE, WIDTH, 576, HEIGHT, 
      268, BGCOLOR, '#333399', CGCOLOR, '#333399', TEXTSIZE, 3 );
  } else { // no duplicates
    submit_continue();
  }
}

