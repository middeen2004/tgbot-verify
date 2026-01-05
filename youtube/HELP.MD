YouTube links look a bit different, for example: https://offers.sheerid.com/youtube/student/?yrdup=https%3A%2F%2Fwww.youtube.com%2F%3Fsld%3Dxxxxxxxxxxxxxxxytpid=premium&ytsku=premium&yrsp=https%3A%2F%2Fwww.youtube.com%2Fpremium%2FstudxxxxxxxxxxxxQQBRgO&euid=230493635&locale=en-US&oid=AI97cxxxxxxxxxxxxxxxxxxxxxNT06Nb5kDzo384b8cAu

The URL does not include SheerID `programId` and `verificationId` fields, so you need to capture the API calls yourself.

Open the network logs and search for `https://services.sheerid.com/rest/v2/verification/`.
Extract `programId` from the request payload and `verificationId` from the response.

Then manually compose the link:
https://services.sheerid.com/verify/xxxxxxxxxx/?verificationId=yyyyyyyyyyy
Here `xxx` is the programId and `yyyy` is the verificationId.
