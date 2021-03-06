<% include("/elements/header.html", "$agentname Tax Report - ".
              ( $beginning
                  ? time2str('%h %o %Y ', $beginning )
                  : ''
              ).
              'through '.
              ( $ending == 4294967295
                  ? 'now'
                  : time2str('%h %o %Y', $ending )
              )
          )
%>
<TD ALIGN="right">
Download full results<BR>
as <A HREF="<% $p.'search/report_tax-xls.cgi?'.$cgi->query_string%>">Excel spreadsheet</A>
</TD>

<% include('/elements/table-grid.html') %>

  <TR>
    <TH CLASS="grid" BGCOLOR="#cccccc" ROWSPAN=3></TH>
    <TH CLASS="grid" BGCOLOR="#cccccc" COLSPAN=9>Sales</TH>
    <TH CLASS="grid" BGCOLOR="#cccccc" ROWSPAN=3></TH>
    <TH CLASS="grid" BGCOLOR="#cccccc" ROWSPAN=3>Rate</TH>
    <TH CLASS="grid" BGCOLOR="#cccccc" ROWSPAN=3></TH>
    <TH CLASS="grid" BGCOLOR="#cccccc" ROWSPAN=3>Tax owed</TH>
% unless ( $cgi->param('show_taxclasses') ) { 
      <TH CLASS="grid" BGCOLOR="#cccccc" ROWSPAN=3>Tax invoiced</TH>
      <TH CLASS="grid" BGCOLOR="#cccccc" ROWSPAN=3></TH>
      <TH CLASS="grid" BGCOLOR="#cccccc" ROWSPAN=3>Tax credited</TH>
      <TH CLASS="grid" BGCOLOR="#cccccc" ROWSPAN=3></TH>
      <TH CLASS="grid" BGCOLOR="#cccccc" ROWSPAN=3>Tax collected</TH>
% } 
  </TR>

  <TR>
    <TH CLASS="grid" BGCOLOR="#cccccc" ROWSPAN=2>Total</TH>
    <TH CLASS="grid" BGCOLOR="#cccccc" ROWSPAN=2></TH>
    <TH CLASS="grid" BGCOLOR="#cccccc" ROWSPAN=1>Non-taxable</TH>
    <TH CLASS="grid" BGCOLOR="#cccccc" ROWSPAN=2></TH>
    <TH CLASS="grid" BGCOLOR="#cccccc" ROWSPAN=1>Non-taxable</TH>
    <TH CLASS="grid" BGCOLOR="#cccccc" ROWSPAN=2></TH>
    <TH CLASS="grid" BGCOLOR="#cccccc" ROWSPAN=1>Non-taxable</TH>
    <TH CLASS="grid" BGCOLOR="#cccccc" ROWSPAN=2></TH>
    <TH CLASS="grid" BGCOLOR="#cccccc" ROWSPAN=2>Taxable</TH>
  </TR>

  <TR>
    <TH CLASS="grid" BGCOLOR="#cccccc"><FONT SIZE=-1>(tax-exempt customer)</FONT></TH>
    <TH CLASS="grid" BGCOLOR="#cccccc"><FONT SIZE=-1>(tax-exempt package)</FONT></TH>
    <TH CLASS="grid" BGCOLOR="#cccccc"><FONT SIZE=-1>(monthly exemption)</FONT></TH>
  </TR>

% my $bgcolor1 = '#eeeeee';
% my $bgcolor2 = '#ffffff';
% my $bgcolor;
%
% foreach my $region ( @regions ) {
%
%   my $link = '';
%   if ( $region->{'label'} eq $out ) {
%     $link = ';out=1';
%   } else {
%     $link = ';'. $region->{'url_param'}
%       if $region->{'url_param'};
%   }
%
%   if ( $bgcolor eq $bgcolor1 ) {
%     $bgcolor = $bgcolor2;
%   } else {
%     $bgcolor = $bgcolor1;
%   }
%
%   #my $diff = 0;
%   my $hicolor = $bgcolor;
%   unless ( $cgi->param('show_taxclasses') ) {
%     my $diff = abs(   sprintf( '%.2f', $region->{'owed'} )
%                     - sprintf( '%.2f', $region->{'tax'}  )
%                   );
%     if ( $diff > 0.02 ) {
%     #  $hicolor = $hicolor eq '#eeeeee' ? '#eeee66' : '#ffff99';
%     #} elsif ( $diff ) {
%       $hicolor = $hicolor eq '#eeeeee' ? '#eeee99' : '#ffffcc';
%     }
%   }
%
%
%   my $td = qq(TD CLASS="grid" BGCOLOR="$bgcolor");
%   my $tdh = qq(TD CLASS="grid" BGCOLOR="$hicolor");
%   my $bigmath = '<FONT FACE="sans-serif" SIZE="+1"><B>';
%   my $bme = '</B></FONT>';

    <TR>
      <<%$td%>><% $region->{'label'} %></TD>
      <<%$td%> ALIGN="right">
        <A HREF="<% $baselink. $link %>;nottax=1"
        ><% &$money_sprintf( $region->{'total'} ) %></A>
      </TD>
      <<%$td%>><FONT SIZE="+1"><B> - </B></FONT></TD>
      <<%$td%> ALIGN="right">
        <A HREF="<% $baselink. $link %>;nottax=1;cust_tax=Y"
        ><% &$money_sprintf( $region->{'exempt_cust'} ) %></A>
      </TD>
      <<%$td%>><FONT SIZE="+1"><B> - </B></FONT></TD>
      <<%$td%> ALIGN="right">
        <A HREF="<% $baselink. $link %>;nottax=1;pkg_tax=Y"
        ><% &$money_sprintf( $region->{'exempt_pkg'} ) %></A>
      </TD>
      <<%$td%>><FONT SIZE="+1"><B> - </B></FONT></TD>
      <<%$td%> ALIGN="right">
        <A HREF="<% $exemptlink. $link %>"
        ><% &$money_sprintf( $region->{'exempt_monthly'} ) %></A>
        </TD>
      <<%$td%>><FONT SIZE="+1"><B> = </B></FONT></TD>
      <<%$td%> ALIGN="right">
        <A HREF="<% $baselink. $link %>;nottax=1;taxable=1"
        ><% &$money_sprintf( $region->{'taxable'} ) %></A>
      </TD>
      <<%$td%>><% $region->{'label'} eq 'Total' ? '' : "$bigmath X $bme" %></TD>
      <<%$td%> ALIGN="right"><% $region->{'rate'} %></TD>
      <<%$td%>><% $region->{'label'} eq 'Total' ? '' : "$bigmath = $bme" %></TD>
      <<%$tdh%> ALIGN="right">
        <% &$money_sprintf( $region->{'owed'} ) %>
      </TD>

% unless ( $cgi->param('show_taxclasses') ) { 
%       my $invlink = $region->{'url_param_inv'}
%                       ? ';'. $region->{'url_param_inv'}
%                       : $link;

        <<%$tdh%> ALIGN="right">
          <A HREF="<% $baselink. $invlink %>;istax=1"
          ><% &$money_sprintf( $region->{'tax'} ) %></A>
        </TD>
        <<%$tdh%>><FONT SIZE="+1"><B> - </B></FONT></TD>
        <<%$tdh%> ALIGN="right">
          <A HREF="<% $creditlink. $invlink %>;istax=1"
          ><% &$money_sprintf( $region->{'credit'} ) %></A>
        </TD>
        <<%$tdh%>><FONT SIZE="+1"><B> = </B></FONT></TD>
        <<%$tdh%> ALIGN="right">
          <% &$money_sprintf( $region->{'tax'} - $region->{'credit'} ) %>
        </TD>
% } 

    </TR>
% } 

</TABLE>

% if ( $cgi->param('show_taxclasses') ) {

    <BR>
    <% include('/elements/table-grid.html') %>
    <TR>
      <TH CLASS="grid" BGCOLOR="#cccccc"></TH>
      <TH CLASS="grid" BGCOLOR="#cccccc">Tax invoiced</TH>
      <TH CLASS="grid" BGCOLOR="#cccccc"></TH>
      <TH CLASS="grid" BGCOLOR="#cccccc">Tax credited</TH>
      <TH CLASS="grid" BGCOLOR="#cccccc"></TH>
      <TH CLASS="grid" BGCOLOR="#cccccc">Tax collected</TH>
    </TR>

%   #some false laziness w/above
%   $bgcolor1 = '#eeeeee';
%   $bgcolor2 = '#ffffff';
%
%   foreach my $region ( @base_regions ) {
%
%     my $link = '';
%     if ( $region->{'label'} eq $out ) {
%       $link = ';out=1';
%     } else {
%       $link = ';'. $region->{'url_param'}
%         if $region->{'url_param'};
%     }
%
%     if ( $bgcolor eq $bgcolor1 ) {
%       $bgcolor = $bgcolor2;
%     } else {
%       $bgcolor = $bgcolor1;
%     }
%     my $td = qq(TD CLASS="grid" BGCOLOR="$bgcolor");
%     my $tdh = qq(TD CLASS="grid" BGCOLOR="$bgcolor");
%
%     #?
%     my $invlink = $region->{'url_param_inv'}
%                     ? ';'. $region->{'url_param_inv'}
%                     : $link;

      <TR>
        <<%$td%>><% $region->{'label'} %></TD>
        <<%$td%> ALIGN="right">
          <A HREF="<% $baselink. $link %>;istax=1"
          ><% &$money_sprintf( $region->{'tax'} ) %></A>
        </TD>
        <<%$td%>><FONT SIZE="+1"><B> - </B></FONT></TD>
        <<%$tdh%> ALIGN="right">
          <A HREF="<% $creditlink. $invlink %>;istax=1"
          ><% &$money_sprintf( $region->{'credit'} ) %></A>
        </TD>
        <<%$td%>><FONT SIZE="+1"><B> = </B></FONT></TD>
        <<%$tdh%> ALIGN="right">
          <% &$money_sprintf( $region->{'tax'} - $region->{'credit'} ) %>
        </TD>
      </TR>

% } 

% if ( $bgcolor eq $bgcolor1 ) {
%   $bgcolor = $bgcolor2;
% } else {
%   $bgcolor = $bgcolor1;
% }
% my $td = qq(TD CLASS="grid" BGCOLOR="$bgcolor");

  <TR>
   <<%$td%>>Total</TD>
   <<%$td%> ALIGN="right">
     <A HREF="<% $baselink %>;istax=1"
     ><% &$money_sprintf( $tot_tax ) %></A>
   </TD>
        <<%$td%>><FONT SIZE="+1"><B> - </B></FONT></TD>
   <<%$td%> ALIGN="right">
     <A HREF="<% $creditlink %>;istax=1"
     ><% &$money_sprintf( $tot_credit ) %></A>
   </TD>
        <<%$td%>><FONT SIZE="+1"><B> = </B></FONT></TD>
   <<%$td%> ALIGN="right">
     <% &$money_sprintf( $tot_tax - $tot_credit ) %>
   </TD>
  </TR>

  </TABLE>

% } 

<% include('/elements/footer.html') %>

<%init>

my $DEBUG = $cgi->param('debug') || 0;

die "access denied"
  unless $FS::CurrentUser::CurrentUser->access_right('Financial reports');

my $conf = new FS::Conf;

my $user = getotaker;

my($beginning, $ending) = FS::UI::Web::parse_beginning_ending($cgi);

my $join_cust =     '     JOIN cust_bill      USING ( invnum  ) 
                      LEFT JOIN cust_main     USING ( custnum ) ';
my $join_cust_pkg = $join_cust.
                    ' LEFT JOIN cust_pkg      USING ( pkgnum  )
                      LEFT JOIN part_pkg      USING ( pkgpart ) 
                      LEFT JOIN cust_location 
                        ON ( cust_location.locationnum = ' .
                        FS::cust_pkg->tax_locationnum_sql . ' )';

my $from_join_cust_pkg = " FROM cust_bill_pkg $join_cust_pkg "; 

my $where = "WHERE _date >= $beginning AND _date <= $ending ";

# this query will be run once per cust_main_county,
# or maybe once per country/state/city tuple,
# or maybe once per country/state...it's hard to say.
my ($location_sql, @base_param) = FS::cust_location->in_county_sql(param => 1);
$where .= " AND $location_sql ";

my $agentname = '';
if ( $cgi->param('agentnum') =~ /^(\d+)$/ ) {
  my $agent = qsearchs('agent', { 'agentnum' => $1 } );
  die "agent not found" unless $agent;
  $agentname = $agent->agent;
  $where .= ' AND cust_main.agentnum = '. $agent->agentnum;
}

sub gotcust {
  my $table = shift;
  my $prefix = @_ ? shift : '';
  "
        ( $table.district = cust_main_county.district
          OR cust_main_county.district = ''
          OR cust_main_county.district IS NULL )
    AND ( $table.${prefix}city  = cust_main_county.city
          OR cust_main_county.city = ''
          OR cust_main_county.city IS NULL )
    AND ( $table.${prefix}county  = cust_main_county.county
          OR cust_main_county.county = ''
          OR cust_main_county.county IS NULL )
    AND ( $table.${prefix}state   = cust_main_county.state
          OR cust_main_county.state = ''
          OR cust_main_county.state IS NULL )
    AND ( $table.${prefix}country = cust_main_county.country )
  ";
}

#non-parameterized form
my $location_in_county = FS::cust_location->in_county_sql;
my $gotcust = "WHERE EXISTS(
  SELECT 1 FROM cust_location WHERE $location_in_county AND disabled IS NULL
)";

my $out = 'Out of taxable region(s)';
# these are actually tax labels, not regions
my %regions = ();

# Phase 1: Taxable and exempt sales
# Collect for each cust_main_county, and assign to a bin based on label.
# Note that "label" includes city if show_cities is on, and taxclass if
# show_taxclasses is on.
foreach my $r ( qsearch({ 'table'     => 'cust_main_county',
                          'extra_sql' => $gotcust,
                          'debug' => $DEBUG,
                       })
              )
{
  warn $r->county. ' '. $r->state. ' '. $r->country. "\n" if $DEBUG > 1;

  # set up a %regions entry for this region's tax label
  my $label = getlabel($r);
  $regions{$label}->{'label'} = $label;

  $regions{$label}->{$_} = $r->$_() for (qw( county state country )); #taxname?

  my @url_param = qw( county state country taxname );
  push @url_param, 'city' if $cgi->param('show_cities') && $r->city();

  $regions{$label}->{'url_param'} =
    join(';', map "$_=".uri_escape($r->$_()), @url_param );

  my @param = @base_param;
  my $mywhere = $where;

  if ( $r->taxclass ) {

    $mywhere .= " AND taxclass = ? ";
    push @param, 'taxclass';
    $regions{$label}->{'url_param'} .= ';taxclass='. uri_escape($r->taxclass);
    #no, always#  if $cgi->param('show_taxclasses');

    $regions{$label}->{'taxclass'} = $r->taxclass;

  } else {

    # SQL for "taxclass doesn't match any other tax in the region"
    my $same_sql = $r->sql_taxclass_sameregion;
    $mywhere .= " AND $same_sql" if $same_sql;

    $regions{$label}->{'url_param'} .= ';taxclassNULL=1'
      if $cgi->param('show_taxclasses')
      || $same_sql;

  }

  # FROM cust_bill_pkg JOIN (whatever is needed to determine tax location)
  # WHERE (matches tax location and agentnum and taxclass)
  # takes parameters in @base_param, plus taxclass if there is one
  my $fromwhere = "$from_join_cust_pkg $mywhere"; # AND payby != 'COMP' ";

  my $nottax = 'pkgnum != 0';

  ## calculate total of sales (non-tax line items) for this region

  my $t_sql =
   "SELECT SUM(cust_bill_pkg.setup+cust_bill_pkg.recur) $fromwhere AND $nottax";
  my $t = scalar_sql($r, \@param, $t_sql);
  $regions{$label}->{'total'} += $t;

  #$regions{$label}->{subtotals}->{$r->taxnum} = $t; #useful debug

  ## calculate customer-exemption for this region

  #false laziness -ish w/report_tax.cgi
  my $cust_exempt;
  if ( $r->taxname ) {
    my $q_taxname = dbh->quote($r->taxname);
    $cust_exempt =
      "( tax = 'Y'
         OR EXISTS ( SELECT 1 FROM cust_main_exemption
                       WHERE cust_main_exemption.custnum = cust_main.custnum
                         AND cust_main_exemption.taxname = $q_taxname
                   )
       )
      ";
  } else {
    $cust_exempt = " tax = 'Y' ";
  }

  my $x_cust = scalar_sql($r, \@param,
    "SELECT SUM(cust_bill_pkg.setup+cust_bill_pkg.recur)
     $fromwhere AND $nottax AND $cust_exempt "
  );

  $regions{$label}->{'exempt_cust'} += $x_cust;
  
  ## calculate package-exemption for this region

  my $x_pkg = scalar_sql($r, \@param,
    "SELECT SUM(
                 ( CASE WHEN part_pkg.setuptax = 'Y'
                        THEN cust_bill_pkg.setup
                        ELSE 0
                   END
                 )
                 +
                 ( CASE WHEN part_pkg.recurtax = 'Y'
                        THEN cust_bill_pkg.recur
                        ELSE 0
                   END
                 )
               )
       $fromwhere
       AND $nottax
       AND (
                ( part_pkg.setuptax = 'Y' AND cust_bill_pkg.setup > 0 )
             OR ( part_pkg.recurtax = 'Y' AND cust_bill_pkg.recur > 0 )
           )
       AND ( tax != 'Y' OR tax IS NULL )
    "
  );
  $regions{$label}->{'exempt_pkg'} += $x_pkg;

  ## calculate monthly exemption (texas tax) for this region

  # count up all the cust_tax_exempt_pkg records associated with
  # the actual line items.

  my $x_monthly = scalar_sql($r, \@param,
    "SELECT SUM(amount)
       FROM cust_tax_exempt_pkg
       JOIN cust_bill_pkg USING ( billpkgnum )
       $join_cust_pkg
     $mywhere"
  );
  $regions{$label}->{'exempt_monthly'} += $x_monthly;

  my $taxable = $t - $x_cust - $x_pkg - $x_monthly;
  $regions{$label}->{'taxable'} += $taxable;

  $regions{$label}->{'owed'} += $taxable * ($r->tax/100);

  if ( defined($regions{$label}->{'rate'})
       && $regions{$label}->{'rate'} != $r->tax.'%' ) {
    $regions{$label}->{'rate'} = 'variable';
  } else {
    $regions{$label}->{'rate'} = $r->tax.'%';
  }
}
warn Dumper(\%regions) if $DEBUG > 1;
# $regions{$label} now contains 'total', 'exempt_cust', 'exempt_pkg', 
# 'exempt_monthly', summed over each set of regions with the same label.

my $distinct = "country, state, county, city, district,
                CASE WHEN taxname IS NULL THEN '' ELSE taxname END AS taxname";
my $taxclass_distinct = 
  #a little bit unsure of this part... test?
  #ah, it looks like it winds up being irrelevant as ->{'tax'} 
  # from $regions is not displayed when show_taxclasses is on
  ( $cgi->param('show_taxclasses')
      ? " CASE WHEN taxclass IS NULL THEN '' ELSE taxclass END "
      : " '' "
  )." AS taxclass";


# Phase 2: invoiced/credited tax items
# Collect this data for each country/state/city/district/taxname(/taxclass).
my %qsearch = (
  'select'    => "DISTINCT $distinct, $taxclass_distinct",
  'table'     => 'cust_main_county',
  'hashref'   => {},
  'extra_sql' => $gotcust,
  'debug' => $DEBUG,
);

# Join to cust_main the same as before (we need agentnum)
# but not to cust_pkg (because tax line items don't have a package)
# and then to cust_location via cust_bill_pkg_tax_location
my $taxfromwhere = "FROM cust_bill_pkg $join_cust 
                    LEFT JOIN cust_bill_pkg_tax_location USING ( billpkgnum )
                    LEFT JOIN cust_location USING ( locationnum )
                    ";
my $taxwhere = $where;

my $creditfromwhere = $taxfromwhere. 
   " JOIN cust_credit_bill_pkg USING (billpkgnum, billpkgtaxlocationnum)";

$taxfromwhere .= " $taxwhere "; #AND payby != 'COMP' ";
$creditfromwhere .= " $taxwhere AND billpkgtaxratelocationnum IS NULL"; #AND payby != 'COMP' ";

#should i be a cust_main_county method or something
# yes. yes, you should.

# $taxfromwhere: Most of a query to find cust_bill_pkg records linked to a 
# customer matching a given state/county/city/district (and within the date 
# range for the report).
# @base_param: A list of the fields from cust_main_county to use as parameters.

# $_taxamount_sub: Takes a cust_main_county and returns the sum of taxes billed
# within the report period for all customers located in that county.  If 
# the cust_main_county has a taxname, limits to taxes with that name; otherwise
# includes all line items with pkgnum = 0 and description either 'Tax' or empty.

my $_taxamount_sub = sub {
  my $r = shift;

  #match itemdesc if necessary!
  my $named_tax =
    $r->taxname
      ? 'AND itemdesc = '. dbh->quote($r->taxname)
      : "AND ( itemdesc IS NULL OR itemdesc = '' OR itemdesc = 'Tax' )";

  my $sql = "SELECT SUM(cust_bill_pkg.setup+cust_bill_pkg.recur) ".
            " $taxfromwhere AND cust_bill_pkg.pkgnum = 0 $named_tax";

  scalar_sql($r, [ @base_param ], $sql );
};

# $_creditamount_sub: As above, but returns the sum of credits applied 

my $_creditamount_sub = sub {
  my $r = shift;

  #match itemdesc if necessary!
  my $named_tax =
    $r->taxname
      ? 'AND itemdesc = '. dbh->quote($r->taxname)
      : "AND ( itemdesc IS NULL OR itemdesc = '' OR itemdesc = 'Tax' )";

  my $sql = "SELECT SUM(cust_credit_bill_pkg.amount) ".
            " $creditfromwhere AND cust_bill_pkg.pkgnum = 0 $named_tax";

  scalar_sql($r, [ @base_param ], $sql );
};

#tax-report_groups filtering
my($group_op, $group_value) = ( '', '' );
if ( $cgi->param('report_group') =~ /^(=|!=) (.*)$/ ) {
  ( $group_op, $group_value ) = ( $1, $2 );
}
my $group_test = sub {
  my $label = shift;
  return 1 unless $group_op; #in case we get called inadvertantly
  if ( $label eq $out ) { #don't display "out of taxable region" in this case
    0;
  } elsif ( $group_op eq '=' ) {
    $label =~ /^$group_value/;
  } elsif ( $group_op eq '!=' ) {
    $label !~ /^$group_value/;
  } else {
    die "guru meditation #00de: group_op $group_op\n";
  }
};

my $tot_tax = 0;
my $tot_credit = 0;
#foreach my $label ( keys %regions ) {
foreach my $r ( qsearch(\%qsearch) ) {

  #warn join('-', map { $r->$_() } qw( country state county taxname ) )."\n";

  my $label = getlabel($r);
  if ( $group_op ) {
    next unless &{$group_test}($label);
  }

  #my $fromwhere = $join_pkg. $where. " AND payby != 'COMP' ";
  #my @param = @base_param; 

  my $x = &{$_taxamount_sub}($r);

  $regions{$label}->{'tax'} += $x;
  $tot_tax += $x unless $cgi->param('show_taxclasses');

  ## calculate credit for this region

  $x = &{$_creditamount_sub}($r);

  $regions{$label}->{'credit'} += $x;
  $tot_credit += $x unless $cgi->param('show_taxclasses');

}

# Phase 3: Non-taxclassed totals for invoiced/credited tax
# (If show_taxclasses is not in use, this was phase 2, but it 
# displays somewhere different.)
# Don't filter by report_groups.
my %base_regions = ();
if ( $cgi->param('show_taxclasses') ) {

  $qsearch{'select'} = "DISTINCT $distinct";
  foreach my $r ( qsearch(\%qsearch) ) {

    my $x = &{$_taxamount_sub}($r);

    my $base_label = getlabel($r, 'no_taxclass'=>1 );
    $base_regions{$base_label}->{'label'} = $base_label;

    $base_regions{$base_label}->{'url_param'} =
      join(';', map "$_=". uri_escape($r->$_()),
                     qw( county state country taxname )
          );

    $base_regions{$base_label}->{'tax'} += $x;
    $tot_tax += $x;

    ## calculate credit for this region

    $x = &{$_creditamount_sub}($r);

    $base_regions{$base_label}->{'credit'} += $x;
    $tot_credit += $x;

  }

}

my @regions = keys %regions;

#tax-report_groups filtering
@regions = grep &{$group_test}($_), @regions
  if $group_op;

#calculate totals
my( $total, $tot_taxable, $tot_owed ) = ( 0, 0, 0 );
my( $exempt_cust, $exempt_pkg, $exempt_monthly, $tot_credit ) = ( 0, 0, 0, 0 );
my %taxclasses = ();
my %county = ();
my %state = ();
my %country = ();
foreach (@regions) {
  $total          += $regions{$_}->{'total'};
  $tot_taxable    += $regions{$_}->{'taxable'};
  $tot_owed       += $regions{$_}->{'owed'};
  $exempt_cust    += $regions{$_}->{'exempt_cust'};
  $exempt_pkg     += $regions{$_}->{'exempt_pkg'};
  $exempt_monthly += $regions{$_}->{'exempt_monthly'};
  $tot_credit     += $regions{$_}->{'credit'};
  $taxclasses{$regions{$_}->{'taxclass'}} = 1
    if $regions{$_}->{'taxclass'};
  $county{$regions{$_}->{'county'}} = 1;
  $state{$regions{$_}->{'state'}} = 1;
  $country{$regions{$_}->{'country'}} = 1;
}

my $total_url_param = '';
my $total_url_param_invoiced = '';
if ( $group_op ) {

  my @country = keys %country;
  warn "WARNING: multiple countries on this grouped report; total links broken"
    if scalar(@country) > 1;
  my $country = $country[0];

  my @state = keys %state;
  warn "WARNING: multiple countries on this grouped report; total links broken"
    if scalar(@state) > 1;
  my $state = $state[0];

  $total_url_param_invoiced =
  $total_url_param =
    'report_group='.uri_escape("$group_op $group_value").';'.
    join(';', map 'taxclass='.uri_escape($_), keys %taxclasses );
  $total_url_param .= ';'.
    "country=$country;state=".uri_escape($state).';'.
    join(';', map 'county='.uri_escape($_), keys %county ) ;

}

#ordering
@regions =
  map $regions{$_},
  sort { ( ($a eq $out) cmp ($b eq $out) ) || ($b cmp $a) }
  @regions;

my @base_regions =
  map $base_regions{$_},
  sort { ( ($a eq $out) cmp ($b eq $out) ) || ($b cmp $a) }
  keys %base_regions;

#add total line
push @regions, {
  'label'          => 'Total',
  'url_param'      => $total_url_param,
  'url_param_inv'  => $total_url_param_invoiced,
  'total'          => $total,
  'exempt_cust'    => $exempt_cust,
  'exempt_pkg'     => $exempt_pkg,
  'exempt_monthly' => $exempt_monthly,
  'taxable'        => $tot_taxable,
  'rate'           => '',
  'owed'           => $tot_owed,
  'tax'            => $tot_tax,
  'credit'         => $tot_credit,
};

#-- 

my $money_char = $conf->config('money_char') || '$';
my $money_sprintf = sub {
  $money_char. sprintf('%.2f', shift );
};

sub getlabel {
  my $r = shift;
  my %opt = @_;

  my $label;
  if (
    $r->tax == 0 
    && ! scalar( qsearch('cust_main_county', { 'district'=> $r->district,
                                               'city'    => $r->city,
                                               'county'  => $r->county,
                                               'state'   => $r->state,
                                               'country' => $r->country,
                                               'tax' => { op=>'>', value=>0 },
                                             }
                        )
               )

  ) {
    #kludge to avoid "will not stay shared" warning
    my $out = 'Out of taxable region(s)';
    $label = $out;
  } else {
    $label = $r->country;
    $label = $r->state.", $label" if $r->state;
    $label = $r->county." county, $label" if $r->county;
    $label = $r->city. ", $label" if $r->city && $cgi->param('show_cities');
    $label = "$label (". $r->taxclass. ")"
      if $r->taxclass
      && $cgi->param('show_taxclasses')
      && ! $opt{'no_taxclass'};
    $label = $r->taxname. " ($label)" if $r->taxname;
  }
  return $label;
}

#my %count_taxname = (); #cache
#sub count_taxname {
#  my $taxname = shift;
#  return $count_taxname{$taxname} if exists $count_taxname{$taxname};
#  my $sql = 'SELECT COUNT(*) FROM cust_main_county WHERE taxname = ?';
#  my $sth = dbh->prepare($sql) or die dbh->errstr;
#  $sth->execute( $taxname )
#    or die "Unexpected error executing statement $sql: ". $sth->errstr;
#  $count_taxname{$taxname} = $sth->fetchrow_arrayref->[0];
#}

#false laziness w/FS::Report::Table::Monthly (sub should probably be moved up
#to FS::Report or FS::Record or who the fuck knows where)
sub scalar_sql {
  my( $r, $param, $sql ) = @_;
  #warn "$sql\n";
  my $sth = dbh->prepare($sql) or die dbh->errstr;
  $sth->execute( map $r->$_(), @$param )
    or die "Unexpected error executing statement $sql: ". $sth->errstr;
  $sth->fetchrow_arrayref->[0] || 0;
}

my $dateagentlink = "begin=$beginning;end=$ending";
$dateagentlink .= ';agentnum='. $cgi->param('agentnum')
  if length($agentname);
my $baselink   = $p. "search/cust_bill_pkg.cgi?$dateagentlink";
my $exemptlink = $p. "search/cust_tax_exempt_pkg.cgi?$dateagentlink";
my $creditlink = $p. "search/cust_credit_bill_pkg.html?$dateagentlink";

</%init>
