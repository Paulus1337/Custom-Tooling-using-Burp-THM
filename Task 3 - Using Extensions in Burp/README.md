## Using Extensions in Burp

### Question:
What is the decoded value for the string `VEhNezEwMUJ1cnB9`?

### Answer:
**THM{101Burp}**  
Notice in the Decoder Improved extension, this is just Base64.

```bash
echo VEhNezEwMUJ1cnB9 | base64 -d

### Question:
Does Burp only offer paid extensions developed by users worldwide?

### Answer:
**Nay**
Burp offers both free and paid extensions. These are available through the BApp Store, and many are developed by the community and shared for free, while others may be commercial or require a license.