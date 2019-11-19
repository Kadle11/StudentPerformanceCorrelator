# StudentPerformanceCorrelator
An Application that Predicts Grades of Students using a Simple Linear Regression Model and an Extremely Ideal Dataset

## Abstract 
The   objective   was   to   build   a   website   that   will   help   teachers   understand   the  
relationship   between   different   subjects   and   extracurricular   activities.   We   wanted   to  
present   an   easy   user   interface   using   which,   the   teachers   could   add   data   regarding  
the   student,   search   for   data   regarding   a   specific   student   and   recognize   the  
correlation   between   different   subjects.   For   example,   if   a   student   is   good   at  
Chemistry,   is   he   likely   to   be   good   at   Biology   as   well?   This   is   what   the   website   helps  
the   teacher   understand.   The   dataset   we   used   has   data   regarding   ~500   students   and  
their   scores   in   Math,   Chemistry,   Computer   Science,   Biology   and   their   interest   in  
Sports.

## Ajax Pattern: Submission Throttling
Using  Submission   Throttling,   you   buffer   the   data   to   be   sent   to   the   server   on   the  
client   and   then   send   the   data   when   the   user   is   idle   for   more   than   a   stipulated  
amount   of   time.   It   doesn't   send   a   request   after   each   character   is   typed.   We   have  
used   this   to   minimize   the   request   while   the   teacher   searches   for   a   student’s  
information.

## Data Science Component: Linear and Logistic Regression
* We   are   using   Linear   Regression   to   predict   the   scores   of   subjects   based   on   the   scores  
of   the   subjects   that   they   have   a   high   correlation   with.   For   instance,   in   our   dataset,   we  
observe   that   Mathematics   and   Computer   Science   have   an   extremely   high  
Correlation.   Hence,   when   either   of   these   scores   are   entered   on   the   “Predict”   page,  
we   use   a   Linear   Regression   model   trained   on   the   dataset   to   predict   the   other  
subject’s score. 
 
* Logistic   Regression   is   used   for   the   category   of   “Sports”.   We   find   that   students   doing  
well   in   Math,   are   interested   in   sports   as   well   and   hence   use   a   logistic   regression  
model   to   predict   whether   a   given   student   is   interested   in   sports,   using   his  
performance in Math

## Uniqueness of the Application
The   application   lets   the   Teacher   not   only   view   the   Student’s   performance,   but   also  
lets   the   teacher   estimate   the   performance   of   a   class   or   a   student   in   one   subject  
using   scores   from   another   subject.   Hence,   the   teacher   can   better   understand   and  
visualize   the   correlation   between   subjects.   It   also   considers   extracurriculars,   such   as  
“Interest in Sports”, as a factor that affects performance in various subjects. 
