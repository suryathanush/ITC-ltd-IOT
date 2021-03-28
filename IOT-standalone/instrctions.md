**CHANGES TO BE MADE**

**CLIENT SIDE CODES :-------------------------------------------------------------------------------------------------------------------------------------------------------------**

1. **speed\_detect\_linked.py :** **(OCR + publisher code)**

        (Publisher linked speed\_detect.py code)

- Line:35 (file path of csv file which is assigned for caching)
- Line:14 (client\_id = &quot;\&lt;any name / or leave as it is\&gt;&quot;)

2. **publisher.py :** (sample publisher code)

- Line:14 (client\_id = &quot;\&lt;any name / or leave as it is\&gt;&quot;)
- Line:27 (file path of csv file which is assigned for caching)
- Line:96 (main\_func())
  - Place in this function all the image processing script that is supposed to be in the forever loop
  - **Example**  **:** if in original OCR code;

                   while(1):
                       print(&quot;hi&quot;)
                       print(&quot;OCR code runs in this loop&quot;)

       Then main\_func() will be like:

                   main_func():
                   print(&quot;hi&quot;)
                   print(&quot;OCR code runs in this loop&quot;)

**Note :** arguments in publish() function should be changed according to the return values of OCR code that are to be transfered

3. **cache\_upload.py :**

- Line:10 (client\_id = &quot;\&lt;any name / or leave as it is\&gt;&quot;)
- Line:81 (file path of csv file which is assigned for caching)
- Line:86 (file path of csv file which is assigned for caching)
- Line:105 (file path of csv file which is assigned for caching)


**SERVER SIDE CODES :------------------------------------------------------------------------------------------------------------------------------------------------------------**

1. **server\_live.py :**

- Line 11-16 (mysql database credentials and port number)
- Line:29 (client\_id = &quot;\&lt;any name / or leave as it is\&gt;&quot;)

2. **server\_cache.py :**

- Line 11-16 (mysql database credentials and port number)
- Line:29 (client\_id = &quot;\&lt;any name / or leave as it is\&gt;&quot;)
