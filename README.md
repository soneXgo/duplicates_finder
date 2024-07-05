  This project is designed for educational practice on the topic: 
"Creating an application to search for duplicate image files in folders" 
together with veemarh.

  As a result of the training practice, the final desktop application has various options and settings for effective 
duplicate search, and the user interacts with the program using a graphical interface. In the course of the work, 
the following tasks were solved.

  We have studied the relevant and in-demand methods of image comparison. The most efficient algorithms 
were built into the final application to find duplicates. The ORB method used, which works on the basis of 
feature extraction and comparison of key points and local descriptors between images, makes it possible to
find absolutely identical and closely similar images. This method is most resistant to various transformations 
such as rotation, scaling, and cropping. Less accurate, but faster, hashing-based algorithms allow you to increase 
the speed of comparing large datasets. In addition, cryptographic hash functions MD5, SHA1 and the SHA-2 family of 
algorithms (SHA-256, SHA-384, SHA-512) were used to search for identical image files. Thus, the user can choose the 
most suitable method for solving their tasks.

  The study of the built-in components of the Python programming language libraries made it possible to quickly and 
conveniently work with the file system and manipulate images. Pillow, OpenCV, imagehash, hashlib, and os libraries 
were used to manage graphical objects, obtain hash values, and interact with the operating system.

  As a result, the code of the program was written, which finds duplicate images depending on the selected options. 
The implemented functions and classes give the user the opportunity to customize the file search, image comparison 
method and processing of the results according to their needs. The following options are built into the application
  1) search: choosing between recursive search and searching only in the source folder; specifying several directories
     to find files; excluding specified directories for image search; detecting files with only specified extensions;
     limiting the properties of the files you are looking for (size, creation time and modification); selecting a
     specific file for which duplicates will be found; 
  2) image comparisons: selection of a comparison algorithm (aHash, pHash, MD5, SHA-1 and others); indication of the
     percentage of similarity of images; search for graphic objects modified with rotations and reflections; indication
     of identical properties that the found duplicates must satisfy relative to the original image;
  3) processing the results: shutting down the program after finding the specified number of duplicates; viewing
     the source file and its duplicates; deleting duplicates and moving them to another folder;

  Based on the results of testing, the following conclusions and recommendations can be made:
    • ORB - the most accurate algorithm, but the slowest; finds copies in different extensions; 
      resistant to rotations, noise, scaling, cropping, lighting changes;
      Recommendation: use on a small dataset.
      
    • aHash - fast, but less resistant to distortion than pHash;
      dHash – resistant to brightness changes, but sensitive to image rotation;
      mHash is more resistant to changes in brightness and contrast than aHash, and is also more resistant to noise 
      and distortion than pHash;
      bHash is resistant to local changes in the image, but less resistant to global transformations;
      pHash (set by default) is the most optimal in terms of accuracy and speed.
      Recommendation: use it for faster (compared to ORB) and more accurate (compared to MD5, SHA-1(160), SHA-256, SHA-384, SHA-512) 
      search for similar images.
      
    • MD5, SHA-1(160), SHA-256, SHA-384, SHA-512 - algorithms are arranged in ascending order of computational cost and accuracy.
      Recommendation: use on a large amount of data to quickly search for absolutely identical images.
