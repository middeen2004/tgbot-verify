# ChatGPT Military SheerID Verification Approach

## 📋 Overview

The ChatGPT military verification flow differs from the student/teacher flow. It requires an extra API call to collect military status before submitting personal information.

## 🔄 Verification Flow

### Step 1: Collect Military Status (`collectMilitaryStatus`)

Call this endpoint before submitting personal information to set the user's military status.

**Request details**:
- **URL**: `https://services.sheerid.com/rest/v2/verification/{verificationId}/step/collectMilitaryStatus`
- **Method**: `POST`
- **Body**:
```json
{
    "status": "VETERAN" // Three options in total
}
```

**Sample response**:
```json
{
    "verificationId": "{verification_id}",
    "currentStep": "collectInactiveMilitaryPersonalInfo",
    "errorIds": [],
    "segment": "military",
    "subSegment": "veteran",
    "locale": "en-US",
    "country": null,
    "created": 1766539517800,
    "updated": 1766540141435,
    "submissionUrl": "https://services.sheerid.com/rest/v2/verification/{verification_id}/step/collectInactiveMilitaryPersonalInfo",
    "instantMatchAttempts": 0
}
```

**Key fields**:
- `submissionUrl`: The URL to use for the next submission step
- `currentStep`: The current step, expected to become `collectInactiveMilitaryPersonalInfo`

---

### Step 2: Collect Personal Information for Non-Active Military (`collectInactiveMilitaryPersonalInfo`)

Use the `submissionUrl` returned from Step 1 to submit personal information.

**Request details**:
- **URL**: Provided in the `submissionUrl` from Step 1  
  - Example: `https://services.sheerid.com/rest/v2/verification/{verificationId}/step/collectInactiveMilitaryPersonalInfo`
- **Method**: `POST`
- **Body**:
```json
{
    "firstName": "name",
    "lastName": "name",
    "birthDate": "1939-12-01",
    "email": "your mail",
    "phoneNumber": "",
    "organization": {
        "id": 4070,
        "name": "Army"
    },
    "dischargeDate": "2025-05-29",
    "locale": "en-US",
    "country": "US",
    "metadata": {
        "marketConsentValue": false,
        "refererUrl": "",
        "verificationId": "",
        "flags": "{\"doc-upload-considerations\":\"default\",\"doc-upload-may24\":\"default\",\"doc-upload-redesign-use-legacy-message-keys\":false,\"docUpload-assertion-checklist\":\"default\",\"include-cvec-field-france-student\":\"not-labeled-optional\",\"org-search-overlay\":\"default\",\"org-selected-display\":\"default\"}",
        "submissionOptIn": "By submitting the personal information above, I acknowledge that my personal information is being collected under the <a target=\"_blank\" rel=\"noopener noreferrer\" class=\"sid-privacy-policy sid-link\" href=\"https://openai.com/policies/privacy-policy/\">privacy policy</a> of the business from which I am seeking a discount, and I understand that my personal information will be shared with SheerID as a processor/third-party service provider in order for SheerID to confirm my eligibility for a special offer. Contact OpenAI Support for further assistance at support@openai.com"
    }
}
```

**Important fields**:
- `firstName`: First name
- `lastName`: Last name
- `birthDate`: Birth date, format `YYYY-MM-DD`
- `email`: Email address
- `phoneNumber`: Phone number (optional)
- `organization`: Military organization details (see list below)
- `dischargeDate`: Discharge date, format `YYYY-MM-DD`
- `locale`: Language/locale, default `en-US`
- `country`: Country code, default `US`
- `metadata`: Metadata containing privacy consent text and related flags

---

## 🎖️ Military Organization List

Available military organization options:

```json
[
    {
        "id": 4070,
        "idExtended": "4070",
        "name": "Army",
        "country": "US",
        "type": "MILITARY",
        "latitude": 39.7837304,
        "longitude": -100.445882
    },
    {
        "id": 4073,
        "idExtended": "4073",
        "name": "Air Force",
        "country": "US",
        "type": "MILITARY",
        "latitude": 39.7837304,
        "longitude": -100.445882
    },
    {
        "id": 4072,
        "idExtended": "4072",
        "name": "Navy",
        "country": "US",
        "type": "MILITARY",
        "latitude": 39.7837304,
        "longitude": -100.445882
    },
    {
        "id": 4071,
        "idExtended": "4071",
        "name": "Marine Corps",
        "country": "US",
        "type": "MILITARY",
        "latitude": 39.7837304,
        "longitude": -100.445882
    },
    {
        "id": 4074,
        "idExtended": "4074",
        "name": "Coast Guard",
        "country": "US",
        "type": "MILITARY",
        "latitude": 39.7837304,
        "longitude": -100.445882
    },
    {
        "id": 4544268,
        "idExtended": "4544268",
        "name": "Space Force",
        "country": "US",
        "type": "MILITARY",
        "latitude": 39.7837304,
        "longitude": -100.445882
    }
]
```

**Organization ID mapping**:
- `4070` - Army
- `4073` - Air Force
- `4072` - Navy
- `4071` - Marine Corps
- `4074` - Coast Guard
- `4544268` - Space Force

---

## 🔑 Implementation Notes

1. **Run steps in order**: Call `collectMilitaryStatus` first. After receiving the `submissionUrl`, call `collectInactiveMilitaryPersonalInfo`.
2. **Organization information**: The `organization` field must include both `id` and `name`. You can randomly select from the list above or let the user choose.
3. **Date formatting**: `birthDate` and `dischargeDate` must use the `YYYY-MM-DD` format.
4. **Metadata**: The `submissionOptIn` field in `metadata` must include privacy policy consent text; extract it from the original request or build it accordingly.

---

## 📝 TODO

- [ ] Implement the `collectMilitaryStatus` API call
- [ ] Implement the `collectInactiveMilitaryPersonalInfo` API call
- [ ] Add military organization selection logic
- [ ] Generate realistic personal information (name, birth date, email, etc.)
- [ ] Generate discharge dates within a sensible range
- [ ] Handle metadata (extract or construct from the original request)
- [ ] Integrate with the main bot command system (e.g., `/verify6`)
