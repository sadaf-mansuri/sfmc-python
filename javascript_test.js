const axios = require('axios');

// Replace these with your actual values
const AUTH_URL = 'https://YOUR_SUBDOMAIN.auth.marketingcloudapis.com/v2/token';
const API_URL = 'https://YOUR_SUBDOMAIN.rest.marketingcloudapis.com/asset/v1/content/assets';
const CLIENT_ID = 'YOUR_CLIENT_ID';
const CLIENT_SECRET = 'YOUR_CLIENT_SECRET';
const ACCOUNT_ID = 'YOUR_ACCOUNT_ID';

// Step 1: Get OAuth token
async function getAuthToken() {
    try {
        const authData = {
            grant_type: 'client_credentials',
            client_id: CLIENT_ID,
            client_secret: CLIENT_SECRET,
            account_id: ACCOUNT_ID
        };

        const authResponse = await axios.post(AUTH_URL, authData, {
            headers: {
                'Content-Type': 'application/json'
            }
        });

        return authResponse.data.access_token;
    } catch (error) {
        console.error('Error fetching auth token:', error);
        throw error;
    }
}

// Step 2: Get email templates with pagination
async function getEmailTemplates(accessToken, page = 1, pageSize = 10) {
    try {
        const headers = {
            Authorization: `Bearer ${accessToken}`,
            'Content-Type': 'application/json'
        };

        const params = {
            $filter: 'assetType.id+eq+207', // filter for email templates
            page,
            pageSize
        };

        const response = await axios.get(API_URL, { headers, params });
        return response.data;
    } catch (error) {
        console.error('Error fetching email templates:', error);
        throw error;
    }
}

// Main function to call both steps
(async function main() {
    try {
        const accessToken = await getAuthToken();
        const emailTemplates = await getEmailTemplates(accessToken);
        console.log('Email Templates:', emailTemplates);
    } catch (error) {
        console.error('An error occurred:', error);
    }
})();
