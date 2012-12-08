
:date: 2012-01-25 17:10:54
:tags: pci
:category: blog
:slug: developers-guide-to-pci-compliant-web-applications
:author: Ken Cochrane
:title: The Developers Guide to PCI Compliant Web applications

*Work in progress last updated: 12-07-2012 by Ken Cochrane*

**Update: 12-07-2012** I have added the youtube video and slides from a recent talk I did on Building PCI Complaint Django Applications.

**Update: 04-05-2012** This article has been `translated into chinese <http://www.ituring.com.cn/article/1372>`_ , by Wujun Shen (吴峻申)


When I first started working at `CashStar.com <http://CashStar.com>`_ three and a half years ago, I had heard about PCI before, but I didn't really know what that meant. Since we were building an ecommerce platform that was going to be accepting credit cards over the internet, I knew we needed to make sure we were fully PCI compliant. We were a startup, we didn't have much money, and any mistake could kill the company. Since I didn't want to be the one to make the mistake, I spent a lot of time doing research on PCI, and what it took to make sure your web application was secure. 

The first thing that I did was a simple web search, and I was surprised to find out that there really wasn't much information available. Most of the information that was available, wasn't easily understandable, and was a little vague. There were companies that you could hire, that would guide you through the process, but since we didn't have much money, they weren't an option for us. So I did what any geek in my situation would do, I spent a bunch of my time reading and researching as much as I could on PCI, and figured my way through the PCI hell, until we were fully PCI compliant. 

My goal with this blog post is write all of my information down, so that I can hopefully help others through the process, and also to serve as a reminder to me, so that when I need to do this again in the future, I will remember every last detail. I hoping to keep this as a sort of live document, and I'll try to keep it up to date as time goes forward and things change. If you notice something is incorrect or I'm missing something, please leave a comment and I'll do my best to update the post as soon as I can.


.. contents:: Quick Links


What is PCI?
-------------------
The first thing most people ask is "What is PCI?". PCI is short for the Payment Card Industry Security Standards Council. PCI consists of American Express, Discover Financial Services, JCB, MasterCard, and Visa, and was formed on Sept 7th, 2006. 

The main purpose of creating the PCI SSC, was to come up with a common set of security standards that merchants could use to better protect themselves against hackers. The PCI SSC came up with the Payment Card Industry Data Security Standard (PCI DSS), which consists of 12 requirements, and many sub-requirements that merchants would need to follow in order to accept debit, credit, prepaid, ATM or POS cards from the PCI SSC members. 

Why was PCI created?
---------------------------------
- It was created in response to a spike in data security breaches.
- It gives merchants a guide to help them make sure they are following best security practices when it comes to card holder data.

Does PCI affect me?
------------------------------
- Do you accept payment online or over the phone with  credit/debit cards?
- Is the credit card information posted to YOUR server?
- Do you store credit card information, encrypted or not?

If you said yes to any of those, then PCI affects you in one way or another. 


PCI DSS Requirements
----------------------------------
Here is the list of 12 requirements. As you look them over, you will notice that most of them aren't that complicated, and you might already be doing thing already. Most of them are just common sense, but it is amazing how many people still don't do things, even if it is common sense.

1. Install and maintain a firewall configuration to protect cardholder data
2. Do not use vendor-supplied defaults for system passwords and other security parameters
3. Protect stored cardholder data
4. Encrypt transmission of cardholder data across open, public networks
5. Use and regularly update anti-virus software on all systems commonly affected by malware
6. Develop and maintain secure systems and applications
7. Restrict access to cardholder data by business need-to-know
8. Assign a unique ID to each person with computer access
9. Restrict physical access to cardholder data
10. Track and monitor all access to network resources and cardholder data
11. Regularly test security systems and processes
12. Maintain a policy that addresses information security

PCI in Layman's Terms
----------------------------------
- All Merchants, regardless if credit card data is stored, must achieve and maintain compliance at all times.
- Merchants cannot store certain credit card information including CVV, track data, magnetic strip or PIN data
- If you store permitted credit card data, you need to store it in a secure way following the PCI security standards.


How does PCI Certification work?
--------------------------------
PCI Certification works like this. If you want to accept credit or debit cards you need to agree that you will maintain PCI certification at all times. There are a couple of ways to confirm that you are certified. You need to either fill out a Self-Assessment Questionnaire (SAQ) or a Report on Compliance (RoC). I'll go over the difference in a little bit, but the important part to remember is that you need to fill out some paper work, and then usually submit that paperwork to whomever requests it, usually the company that processes your credit cards and handles your merchant account.

 - Fill out a Self-Assessment Questionnaire (SAQ) and Find out what level you are
 - Make sure you follow all recommendations for that level
 - Fix any issues
 - Attestation of Compliance (if self assessing)
 - External Auditor (if needed)


How to get started?
----------------------------
 1. Identify the individuals that will be responsible for PCI compliance in your organization and assemble a team that includes members from each area.
 2. Determine your merchant level (1-4).
 3. Determine which SAQ your organization will need to complete.
 4. Evaluate whether your organization will try to achieve compliance internally or engage with aQualified Security Assessor (QSA).
 5. Engage with an Approved Scanning Vendor (ASV) to start the required external IP vulnerability scans.
 6. Make sure that your organization has an Information Security Policy and that it is being enforced.
 7. Immediately address any significant deficiencies discovered during the assessment or scan.
 8. Retain record of self-assessments, scans, and follow-up activities. Be prepared to provide these documents upon request.



What PCI Level am I?
--------------------------------
There are 4 PCI compliance level's, and how many transactions you process a year will determine which level you are in.

Merchant Level
~~~~~~~~~~~~~~

**Level 1** : Merchants processing over 6 million Visa transactions annually (all channels) or Global merchants identified as Level 1 by any Visa region

**Level  2** : Merchants processing 1 million to 6 million Visa transactions annually (all channels)

**Level  3** : Merchants processing 20,000 to 1 million Visa e-commerce transactions annually

**Level 4** : Merchants processing less than 20,000 Visa e-commerce transactions annually and all other merchants processing up to 1 million Visa transactions annually

Requirements
~~~~~~~~~~~~
**Level 1** : Onsite Security Assessment Required Annually, Network Vulnerability Scan required Quarterly

**Level 2** : Onsite Security Assessment at Merchants Discretion, Self-Assessment Questionnaire Required Annually, Network Vulnerability Scan Required Quarterly

**Level 3** : Self-Assessment Questionnaire Required Annually, Network Vulnerability Scan Required Quarterly

**Level 4** : Self-Assessment Questionnaire Required Annually, Network Vulnerability Scan Required Quarterly

RoC or SAQ?
--------------------
If you are a Level 1 then you need to fill out a RoC, if you are level 2, 3 or 4, then you can fill out an SAQ. There are some exceptions to these rules, for example, if you have had a security breach in the past, the credit card companies might require that you complete a RoC even if you aren't a level 1. 


Report on Compliance (RoC)
--------------------------------
If you process more than six million credit cards per year (Level 1), you are required to have an on-site PCI assessment and Report on Compliance (RoC) issued by a Qualified Security Assessor (QSA). Other Level 2 organizations may also be required to submit a RoC or choose to do so in anticipation of becoming a Level 1 merchant.

QSA’s can be engaged to provide this annual review.  It includes a review of established processes and procedures for networks, servers and databases in scope for PCI compliance.  The engagement involves interviews with stakeholders in your organization, a review of supporting documentation, validation of compliance initiatives and completion of the report itself.

QSA’s usually encourage their PCI Customers to use a PCI compliance management solution throughout the year.  This will assist them with maintaining compliance and should make the on-site engagement and the completion of the RoC faster and smoother.


Self-Assement Questionnaire
-------------------------------------------
There are 5 SAQ categories, depending on which category that you fall into, the paper work might be real easy, it might take a lot longer. Here are the 5 categories.

**SAQ-A** : Card-not-present (e-commerce or mail/telephone-order) merchants, all cardholder data functions outsourced.  This would never apply to face-to-face merchants.

**SAQ-B** : Imprint-only merchants with no electronic cardholder data storage, or standalone, dial- out terminal merchants with no electronic cardholder data storage

**SAQ-C-VT** : Merchants using only web-based virtual terminals, no electronic cardholder data storage

**SAQ-C** : Merchants with payment application systems connected to the Internet, no electronic cardholder data storage

**SAQ-D** : All other merchants not included in descriptions for SAQ types A through C above, and all service providers defined by a payment brand as eligible to complete an SAQ.

Since we are only talking about web applications here, you will most likely only fall into either A, C, or D. Once you know your level you will need to fill out the SAQ for that category. Once you are done you need an Attestation of compliance as well. 

Here is a helpful guide to help you figure out what category you a fall into.

SAQ-A
~~~~~

There are a lot of different parts to A, but the big one, is that the credit card data never touches your servers. The easiest way to do this is to redirect people to someone else's servers when you want them to enter credit card data. This is common with Paypal, google checkout and Amazon payments. 

Another way around this is to have your payment page hosted by your credit card gateway. An example of this is authorize.net's `Simple Checkout <http://www.authorize.net/solutions/merchantsolutions/merchantservices/simplecheckout/>`_. 

A third way of doing this is what is called "transparent redirect" or "Direct Post", `BrainTreePayments <http://www.braintreepayments.com/services/pci-compliance>`_ was the first to make this popular, but since then `Authorize.net <http://developer.authorize.net/api/dpm>`_  has also added it.

And finally the last way, is basically similar to the third way, but it uses javascript to encrypt the credit card data, send it to the credit card processor, and then populate the form with unique tokens, which will be used later on. This approach is used by `stripe <http://stripe.com>`_.

BrainTree + livingsocial talk about this new approach of `end to end encryption of credit card data <http://www.braintreepayments.com/devblog/end-to-end-encryption>`_.


SAQ-C
~~~~~

If you are hosting the payment form on your own server, and when you hit submit on that form it goes to your server, where you parse the form, get the credit card details out of the fields, build up your request and then send it to the credit card processor yourself. Then you are at least a C. Even if you aren't storing the data, because it is available in your computer memory, and you are touching it with your code, there is risk that something could happen and you would be able to get access to the credit card data.

SAQ-D
~~~~~

If you don't fall into the other categories then you are a D. SAQ D is sometimes referred to as ROC light, because any organization that has to fill out SAQ D is essentially going through all 12 PCI DSS requirements, albeit on a reduced scale.


How much does PCI Cost?
---------------------------------------
It is really hard to get an accurate value for this because it will be different for everyone, but according to BrainTree here is a chart on `how much it costs to become PCI Compliant <http://www.braintreepayments.com/blog/what-does-it-cost-to-become-pci-compliant>`_.

=====    ==========  ======== ===========    ==========
Level    # of Trans  Scope    Compliance     Audit type
=====    ==========  ======== ===========    ==========
1        6M+         $125K    $586K          onsite
2        1M-6M       $105K    $267K          SAQ
3        20K-1M      $44K     $81K           SAQ
4        < 20K       ?        ?              SAQ
=====    ==========  ======== ===========    ==========


External Audits
----------------------

=======   =================
Level     Cost Per Year
=======   =================
Low End   $20K-$30K
Average   $225K
Top 10%   $500K+
=======   =================


If you are big enough or unlucky enough to require an external audit, it isn't going to be cheap. Audits last a few weeks or more onsite, and cost anywhere from $20K-$30K on the low end.  They average around $225K a year, and about 10% of the audits cost over $500K. As you can see this is a really expensive annual cost, and should be avoided if possible. 

It is also important to point out that this is just the cost of the audit itself, if they find anything wrong in the audit, you will need to pay to fix any of the issues before they will certify you. 

Here are some links where I got my data.
 - http://www.networkworld.com/news/2010/030110-pci-compliance-audit-cost.html
 - http://blog.elementps.com/element_payment_solutions/2009/02/pci-compliance-costs.html
 - https://www.infosecisland.com/blogview/12356-Five-Questions-to-Ask-Your-PCI-Auditor-Before-You-Hire-Them.html



PCI 2.0
-----------
On October 26th 2010, PCI DSS version 2.0 was released. Here are some of the highlights.

- 132 changes, 2 new ones, the rest are clarifications or additional guidelines
- Added more guidelines around virtualization, and how it affects PCI
- Amazon web services (AWS) is now a Level 1 PCI compliant data center.



Nitty Gritty
------------
Now that you know what PCI is all about, lets get down to the nitty gritty. The most common questions I'm asked is what is the easiest way to become PCI certified. Here is what I tell people. 

First off, avoid handling credit card data if you can help it. It has become a lot easier lately with Braintree and stripe. Years ago before these solutions were available, the only way to do it was to use an ugly hosted payment page on your credit card gateway, and it wasn't very good, and hard to integrate, so most people didn't use those solutions. 

Now you have no excuse, let the credit card processor handle all of the credit card data, and it will make your life easier. If you want to see how much easier, go to the `PCI security standards <https://www.pcisecuritystandards.org>`_ website and download the `SAQ A <https://www.pcisecuritystandards.org/documents/pci_saq_a_v2.doc>`_ and the `SAQ C <https://www.pcisecuritystandards.org/documents/pci_saq_c_v2.doc>`_ docs. You will notice that the SAQ A is much easier, and a lot less of a hassle. 

As great as the Briantree and stripe solutions are they can't solve all problems. One common problem is accepting credit card data over an API, more and more common these days with mobile applications. If you can't use one of the other solutions for one reason or another, you can check out `Edge Tokenization <http://www.akamai.com/html/solutions/security/edge_tokenization.html>`_ from Akamai, it will work for both API and web based payment forms. It is pretty expensive, but if you are already using some of akamai's other solutions then this might not be as big of an issue.

If you still need/want to accept credit card data on your own server after everything that I said above, then you are going to need to know about some other things. For example, here are a list of common mistakes that most people make.

Common PCI Mistakes
-------------------
Here is a list of common mistakes most people make. I'm listing them here so that you can catch these mistakes before it is too late. If I missed any, let me know.


Storing credit card information in plain text
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Ideally, you should never store credit card information, but if you have to, you should always
encrypt the data, so that if someone gets ahold of your data, they won't be able to see it unless
they put in a lot of effort. 


Default passwords not changed
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
I'm always surprised to here how weak peoples passwords are, and how most of the time they are still using the first one that was given to them when they started. That is why if you are the one generating a password, make it a secure one, so that if the people don't change the password like you told them too, it will at least be a secure one to begin with. 

There are really good password management tools on the market today, I recommend using one of them. One of my favorites is `1password <https://agilebits.com/onepassword>`_.


Remove all programs not needed from your servers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
There are a couple reasons why you would want to remove any programs/software from your computer if you are not using it. The first one, it will take up less space, and if it isn't running it will free up processor and RAM, a faster system is always good. The second reason is so that you don't have to maintain the security patches for something you aren't using. So, the first step you should do when you bring a new server online is to remove all of the stuff you aren't using. You can always add it back later.

Use a Firewall
~~~~~~~~~~~~~~
You should always use a firewall, it doesn't matter if it is a hardware firewall or a software firewall, use it, and never turn it off. In some of my production systems I run both a hardware firewall coming into my private network and then a software firewall on each system. Some people think this is overkill, but I would rather be safer then sorry.

Just running the firewall is only part of it, you need to know how the firewall is setup, and why. You should always have a document around with a list of which ports are open and why. This will be very helpful later on, when you get audited and they want to know what ports are open, and the reasons for it. 

You should do a quarterly review of your firewalls to make sure they match your documentation, and to see if any of the ports that were previously open still need to be open. Systems change over time, and sometimes you will remove a service that isn't needed anymore, and when that happens you should also block the port.

You could also use a service like `CloudFlare <http://cloudflare.com>`_ that protect your website from a range of online threats from spammers to SQL injection to DDOS. It is easy to setup, and your code changes should be minimal at most.

Poorly coded websites
~~~~~~~~~~~~~~~~~~~~~
If the programmers who are writing your web application aren't careful, and don't know what they are doing, they could write bad code which could result in SQL injection and other vulnerabilities.  

Cross Site Scripting (XSS) is becoming a more and more common way of attacking websites these days, so make sure you are careful of that as well. 

Make sure you always conduct code reviews, and use application penetration testing before you put your code into production.

Lack of monitoring and logging
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
It is amazing how many companies have no system or application monitoring, it is like they are running blind, they have no idea when something is going wrong until their customers tell them. You should have as much monitoring and logging as possible, so that you know what is happening with your system at all times. If you don't log when things are going well, then when stuff starts going bad you will have no idea what things are suppose to look like when things are good.

Here is a list of tools that will help you with your logging and monitoring.

- `Pingdom <http://pingdom.com>`_ Is a website monitoring tool, they will tell you when your site is down.
- `Nagios <http://www.nagios.org/>`_ offers complete monitoring and alerting for servers, switches, applications, and services.
- `Cacti <http://www.cacti.net/>`_ is a complete network graphing solution designed to harness the power of RRDTool's data storage and graphing functionality.
- `Sentry <https://github.com/dcramer/sentry>`_ Open Source realtime event logging and aggregation platform
- `Loggly <http://loggly.com/>`_ Log management cloud service for centralized log search and analysis, time series data.
- `graphite <http://graphite.wikidot.com/>`_ Scalable Realtime Graphing server
- `collectd <http://collectd.org/>`_ is a daemon which collects system performance statistics periodically and provides mechanisms to store the values in a variety of ways, for example in RRD files.
- `monit <http://mmonit.com/>`_ Easy, proactive monitoring of Linux/Unix systems, network and cloud services. 
- `munin <http://munin-monitoring.org/>`_ Munin is a networked resource monitoring tool that can help analyze resource trends.
- `New Relic <http://NewRelic.com>`_ is the only tool you need to pinpoint and solve performance issues in your Ruby, Java, .NET, PHP and Python apps.
- `Pager Duty <http://PagerDuty.com>`_ Phone & SMS alerting and on-call scheduling for Nagios, Zenoss, Munin, Monit, and most other IT monitoring tools.


Missing security patches
~~~~~~~~~~~~~~~~~~~~~~~~
It is important that you regularly schedule applying all security patches on all of your systems. This is a no brainer but it is amazing how much this doesn't happen.

You should also subscribe to all of the security alert email lists for any of the products that you are using, as well as paying attention the following list of websites below. The sooner you get notified of a potential problem the sooner you can fix it before it effects you. 

- http://www.us-cert.gov/cas/
- http://seclists.org/
- http://www.sans.org/newsletters/


Not using SSL for payment page
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Another no brainer, but sometimes it happens. You should add code to your web applications that check to make sure that the payment pages are served over SSL, if not, do a redirect to the SSL version of the page. 

An easy way to do this is to serve the whole site over SSL all of the time, and then do a simple redirect with your web server from port 80 (http) over to port 443(https). This will guarantee that all traffic is served over SSL all of the time. 


Logging payment information 
~~~~~~~~~~~~~~~~~~~~~~~~~~~
One of the most common mistakes that I see is when someone has their logging setup to print out data from the payment form to the logs. This is great for debugging purposes but bad for PCI. You should always strip out the important information out of the request before logging it. You can replace the credit card number with \**last4 and get the same result.

Another common mistake that is similar is dumping all of the data when there is an error and emailing it to the developers. If you do this as well, make sure you strip out the credit card info first or else that person's credit card information is now emailed all over the place, which isn't good at all.


Credit card data that can be stored
--------------------------------------------------
It is important that you NEVER EVER store credit card information in the database, even if it is encrypted. It isn't worth the hassle, risk and the cost of handling an external audit. But if you absolutely insist, here is something you need to know.

If for some reason you ignore my advice and decide to store credit card data anyway, here is a little chart that will show you which data is allowed to be stored, and If it needs to be encrypted or not.

- According to 3.3 Mask PAN when displayed (the first six and last four digits are the maximum number of digits to be displayed). That means, you need to do something like this \*****1234 Visa instead of the actual credit card number. This is pretty common these days.

- According to 3.4 : Render PAN unreadable anywhere it is stored (including on portable digital media, backup media, and in logs) by using any of the following approaches:

    - One-way hashes based on strong cryptography (hash must be of the entire PAN) [ One-way hash functions such as the Secure Hash Algorithm (SHA) based on strong cryptography can be used to render cardholder data unreadable. Hash functions are appropriate when there is no need to retrieve the original number (one-way hashes are irreversible) To complicate the creation of rainbow tables it is recommended, but not a requirement, that a salt value be input to the hash function in addition to the PAN.] 
    - Truncation (hashing cannot be used to replace the truncated segment of PAN)
    
    - Index tokens and pads (pads must be securely stored)
    
    - Strong cryptography with associated key-management processes and procedures



+------------------+-------------------+-----------------------+
|                  | Storage Permitted | Protection Required   |
+==================+===================+=======================+
|                   **Cardholder Data**                        |
+------------------+-------------------+-----------------------+
| Account Number   |        Y          |          Y            |
+------------------+-------------------+-----------------------+
| Cardholder data  |        Y          |          N            |
+------------------+-------------------+-----------------------+
| Expiration Date  |        Y          |          N            |
+------------------+-------------------+-----------------------+
| Service Code     |        Y          |          N            |
+------------------+-------------------+-----------------------+
|                    **Authentication Data**                   |
+------------------+-------------------+-----------------------+
| Magnetic Strip   |        N          |         n/a           |
+------------------+-------------------+-----------------------+
| CVV              |        N          |         n/a           |
+------------------+-------------------+-----------------------+
| Pin Data         |        N          |         n/a           |
+------------------+-------------------+-----------------------+ 


Tokenization
-------------------
If you need to store credit card information, it is best to use a `tokenization <http://en.wikipedia.org/wiki/Tokenization_(data_security)>`_ service instead of storing it yourself. You store the credit card information in their system. They give you a unique token that you use for all future transactions against that credit card. These types of service are pretty common these days, just ask your credit card processor if they have such a service. Here are a couple of credit card processors that provide this sort of service.

- `Authorize.net CIM <http://www.authorize.net/solutions/merchantsolutions/merchantservices/cim/>`_
- `BrainTree Vault <http://www.braintreepayments.com/services/payment-gateway>`_
- `Stripe.com <https://stripe.com/docs/stripe.js>`_
- `Recurly.com subscription based billing <http://recurly.com>`_


Data Centers
-------------------

When you are dealing with PCI compliance you need to worry about the full stack, not just your application, but also the server the application lives on, the network your server is connected to, and the data center your server lives in. The first thing you will want to do is contact your your hosting provider to see if they are PCI compliant, and if so, you might want to request a copy of their PCI documents for your records (you might need them later). Usually hosting providers that are PCI compliant brag about it on their web pages, so that is usually a good place to start. 

The smaller the hosting company that you deal with the smaller the chance you will be PCI compliant. If you are just using a shared hosting plan, and paying $20/month, most likely you are not compliant. You might get lucky, but I doubt it. If you are using a PAAS or a cloud provider, you will also most likely be out of luck. 



Hosting in the Cloud
-----------------------------
`Amazon Web Services <http://aws.amazon.com>`_ (AWS) has recently had their data centers meet PCI compliance, but what is important to note is that just because the data center in compliant, doesn't mean that your application is going to be. If you put your application on EC2, and you accept credit card data that is getting processed on those EC2 instances, you will need to make sure that you also have an Intrusion Detection System (IDS) amongst other things in place or else you aren't PCI compliant. All of the good IDS's are hardware based, and have someone monitoring the traffic at all times. You can't install those systems in AWS, so you will need to rely on a software based solution, which isn't as good, and adds another layer of complexity to your network stack.

`RackSpace <http://Rackspace.com>`_ offers a `hybrid cloud hosting <http://www.rackspace.com/hosting_solutions/hybrid_hosting/>`_ setup, which allows you to have hardware firewall, IDS, Load balancers, cloud web servers and hardware database servers. But even in this setup, it isn't PCI compliant, at least I haven't been able to get RackSpace to tell me it is yet. 

There are other cloud providers that might be able to offer you a complete PCI compliant solution, but I'm guessing they are going to cost more money. If you know of one, please let me know and I'll update this. `Terremark <http://www.terremark.com/services/security-services/governance-risk-compliance-management/pci-compliance.aspx>`_ might have something. 



Security Scanners
---------------------------
A key part of the PCI certification is the 3rd party security scanning requirement. Basically you have to pay one of the certified and approved security scanning companies to scan you network, server, application every so often, and if it finds any issues, you will need to fix those, and scan again until you pass their tests. Once you pass the scans they will give you a certificate that you can attach to the rest of your PCI documentation.

I have used a company called `ControlScan <http://www.controlscan.com>`_ in the past, and I have also used `Qualys <http://www.qualys.com>`_, but I'm sure there are a ton of others out there. Pick the one that looks the best for you. Here is a link to a list of `PCI approved scanning vendors <https://www.pcisecuritystandards.org/approved_companies_providers/approved_scanning_vendors.php>`_



Intrusion Detection Systems
----------------------------------------
Intrusion Detection Systems (IDS) basically sit in front of your network and watch all of the network traffic coming into your network. It looks to see if it notices anything out of the ordinary, of if people are trying to use known attacks, and if it finds something it will let you know. They have hard ware and software based solutions. They range in price from free to thousands of dollars a month. They all have different features and abilities, it is best to pick one that has what you need, that you are comfortable maintaining. 

I have used `AlertLogic's <http://www.alertlogic.com>`_ hardware based IDS, and it works well. They have a pool of on call people who monitor the devices and if something gets triggered they look it over, and act accordingly. 


Hashing credit card numbers
------------------------------------------
Here is a great example on why hashing credit card numbers isn't a good idea. I'm borrowing some of this from these two links.
 
- http://en.oreilly.com/rails2011/public/schedule/detail/19466
- http://www.integrigy.com/security-resources/whitepapers/Integrigy_Hashing_Credit_Card_Numbers_Unsafe_Practices.pdf

Just because you are following PCI rules doesn’t mean you are invincible, you still have to use your common sense.

 PCI DSS section 3.4 `[pdf] <http://www.pcisecuritystandards.org/pdfs/pci_audit_procedures_v1-1.pdf>`_: 
 Render PAN, at minimum, unreadable anywhere it is stored .. by using any of the following approaches: Strong one-way hash functions (hashed indexes)

 Verify that data is rendered unreadable using one of the following methods: one-way hashes (hashed indexes) such as SHA-1

 Basically what this is saying is that you are allowed to store the first 6 digits of a credit card (BIN) as well as the last 4 digits of the credit card. Credit cards are between 13-16 digits in length and the last digit is the check digit (`Luhn algorithm <http://en.wikipedia.org/wiki/Luhn_algorithm>`_). 

Let's see how hard it would be to figure out this credit card number. 4012888888881881

If we start with a full 16 digits that means that we have ￼10^16 or 10,000,000,000,000,000 (10 Quadrillion) Possible Card Numbers, if we didn't know anything about the card.

Since we are storing the credit card type, we know this is a visa, visa credit cards all start with a 4 so that means that is could be 4XXXXXXXXXXXXXXX or ￼4,000,000,000,000,000 (4 Quadrillion) Possible Card Numbers, we just cut the number of possible cards in more then half. 

If we also store the bin (first 6 digits) and the last 4 digits, then it would look like this. 401288******1881 or 1,000,000 (1 million) possible card numbers.

Starting with that lets try to write a simple cracker (Ruby)

.. code-block:: ruby

    hashed_card_number = '62163a017b168ad4a229c64ae1bed6ffd5e8fb2d'
    masked_card_number = '401288******1881'

Code

.. code-block:: ruby

    require 'digest/sha1'
    
    def reverse_hashed_card_number( hashed_card_number, first_six, last_four)
        0.upto(999_999) do |i|
            card_number_to_test = "#{first_six}%06d#{last_four}" % i
            hashed_to_test = Digest::SHA1.hexdigest(card_number_to_test)
            if hashed_card_number == hashed_card_number_to_test
              return card_number_to_test
            end
        end
    end
    
Let's run it

.. code-block:: ruby

    Benchmark.measure do
      puts reverse_hashed_card_number(
        '62163a017b168ad4a229c64ae1bed6ffd5e8fb2d',
        '401288',
        '1881'
    ) end.real
    4012888888881881
    => 5.33522081375122

In 5.3 seconds it was able to crack the hash, if you use only a SHA-1 hash. We could possibly make it even faster if we did a luhn check on the number before we ran the hash, and if the luhn check fails then we know the number isn't valid and there is no need to run the hash. Since the hash function is going to be slower then the luhn check it should speed things up. 

Rainbow Tables + Salts
------------------------
Since we know that there is a finite number of credit cards, we could pre-calculate the hash code for every single one of the 10 Quadrillion possible card values, and store those in a lookup table. Then when ever I wanted to crack a credit card hash, all i would need is the credit card hash, and I would be able to figure out the value of that card, very quickly. Storing all of the known values in a table like this is called a `Rainbow table <http://en.wikipedia.org/wiki/Rainbow_tables>`_.

Ideally if you are going to hash a credit card, don't use SHA-1, or MD5, use one of the newer SHA versions, SHA-256 or above, and also use a `salt <http://en.wikipedia.org/wiki/Salt_(cryptography)>`_. A salt is basically a second unique value that you always use when hashing, to generate a different salt then you would normally get with just the credit card number. 

Since I won't have your salt when I generate my rainbow table, my rainbow table will be no good. It adds yet another layer of security. Make sure you don't lose your SALT or else you will have to start over from scratch. Treat your salt like a password, and keep it safe.

Do I really have to worry about being hacked?
---------------------------------------------
Here is a short list of companies that have been hacked recently. If they can get hacked, so could you. 

- `TJ Maxx <http://en.wikipedia.org/wiki/T.K._Maxx#2007_credit_card_fraud>`_
- Bank of America
- Citigroup
- BJ's wholesale club
- Hotels.com
- LexisNexis
- Polo Ralph Lauren
- Wachovoa
- `Heartland Payment Systems <http://en.wikipedia.org/wiki/Heartland_Payment_Systems#Security_breach>`_
- Hannaford

What could happen if you were Hacked?
----------------------------------------------------------
- Banned from accepting credit cards
- Loss of reputation and customers
- Fines up to $500,000 per incident
- Litigation (you could be sued)

What if I was breached?
-----------------------------------
In the event of a security incident, merchants must take immediate action to:

1. Contain and limit the exposure. Conduct a thorough investigation of the suspected or confirmed loss or theft of account information within 24 hours of the compromise
2. Alert all necessary parties. Be sure to notify: * Merchant Account Provider * Visa Fraud Control Group at (650) 432-2978 * Local FBI Office * U.S. Secret Service (if Visa payment data is compromised)
3. Provide the compromised Visa accounts to Visa Fraud Control Group within 24 hours.
4. Within four business days of the reported compromise, provide Visa with an incident report.

Build PCI Complaint Django Applications
---------------------------------------
I recently gave a talk on Build PCI Complaint Django Applications, at DjangoCon US 2012 in Washington D.C. Here are my slides and the video of my talk.

Slides
~~~~~~

.. html::
    <div style="width: 710px;height: 612px;" id="slides_container">
    <script async class="speakerdeck-embed" data-id="5048f7b290b276000202452f" data-ratio="1.2994923857868" src="//speakerdeck.com/assets/embed.js"></script>
    </div>

Video
~~~~~

.. html::

    <iframe width="640" height="360" src="http://www.youtube.com/embed/9ZIPNWqjIEI?rel=0" frameborder="0" allowfullscreen></iframe>


Links:
--------
- `Akamai edge tokenization <http://www.akamai.com/html/solutions/security/edge_tokenization.html>`_
- `PCI Security Standards <https://www.pcisecuritystandards.org>`_
- `American Express PCI pages <http://www.americanexpress.com/datasecurity>`_
- `Discover Financial Services PCI pages <http://www.discovernetwork.com/fraudsecurity/disc.html>`_
- `JCB International PCI pages <http://www.jcb-global.com/english/pci/index.html>`_
- `MasterCard Worldwide PCI pages <http://www.mastercard.com/sdp>`_
- `Visa Inc PCI pages <http://www.visa.com/cisp>`_
- `Visa Europe PCI pages <http://www.visaeurope.com/ais>`_



