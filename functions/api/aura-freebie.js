const MAILERLITE_API = 'https://connect.mailerlite.com/api/subscribers';

const GROUPS = [
  '190911925163394566', // Aura Freebie Subscribers
  '190911926663906901', // Tag - Aura Interest
  '190911927182952115', // Tag - Downloaded Aura Freebie
];

function response(body, init = {}) {
  return new Response(body, {
    ...init,
    headers: {
      'content-type': 'text/html; charset=UTF-8',
      'cache-control': 'no-store',
      ...(init.headers || {}),
    },
  });
}

function errorPage(title, message, status = 400) {
  return response(`<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>${title} | Soft Moon Studio</title>
  </head>
  <body>
    <main style="font-family: system-ui, sans-serif; max-width: 38rem; margin: 4rem auto; padding: 0 1rem; line-height: 1.55;">
      <h1>${title}</h1>
      <p>${message}</p>
      <p><a href="/aura-freebie/">Return to the workbook form</a></p>
    </main>
  </body>
</html>`, { status });
}

function redirect(request, location) {
  return Response.redirect(new URL(location, request.url), 303);
}

function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

export async function onRequestPost(context) {
  const token = context.env.MAILERLITE_API_TOKEN;
  if (!token) {
    return response('MailerLite is not configured.', { status: 500 });
  }

  const form = await context.request.formData();
  const email = String(form.get('email') || '').trim().toLowerCase();
  const name = String(form.get('name') || '').trim();
  const source = String(form.get('source') || 'aura_freebie').trim();

  if (!isValidEmail(email)) {
    return errorPage('Please check your email address', 'The email address did not look valid. Please go back and try again.');
  }

  const fields = {
    source,
  };

  if (name) {
    fields.name = name;
  }

  const mailerliteResponse = await fetch(MAILERLITE_API, {
    method: 'POST',
    headers: {
      accept: 'application/json',
      authorization: `Bearer ${token}`,
      'content-type': 'application/json',
    },
    body: JSON.stringify({
      email,
      fields,
      groups: GROUPS,
      status: 'active',
    }),
  });

  if (!mailerliteResponse.ok) {
    const message = await mailerliteResponse.text();
    console.error('MailerLite subscribe failed', mailerliteResponse.status, message);
    return errorPage(
      'Something went wrong',
      'The workbook form could not connect to the email system. Please try again in a few minutes.',
      502,
    );
  }

  return redirect(context.request, '/aura-freebie-thank-you/');
}

export function onRequestGet(context) {
  return redirect(context.request, '/aura-freebie/');
}
