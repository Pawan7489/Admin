// File: edge/deno_router.ts
// Purpose: The "Flash" Layer. Handles high-speed requests at the Edge.
// Free Limit: 100,000 requests/day.

import { serve } from "https://deno.land/std@0.177.0/http/server.ts";

console.log("⚡ [Deno]: Edge Node Active. Waiting for requests...");

serve(async (req) => {
  const url = new URL(req.url);
  
  // 1. Instant Health Check (0ms Latency feel)
  if (url.pathname === "/status") {
    return new Response(
      JSON.stringify({ 
        system: "A1 OS", 
        status: "Online", 
        location: "Edge Network (Global)" 
      }),
      { headers: { "Content-Type": "application/json" } }
    );
  }

  // 2. Heavy Request Routing (Render ki taraf bhejo)
  // Agar user kuch bhaari puchta hai, toh use Python server par forward karo
  if (url.pathname === "/ask_ai") {
    const python_server = "https://a1-os-admin.onrender.com/ask_ai";
    
    // Redirect user to the main brain transparently
    return Response.redirect(python_server, 307);
  }

  return new Response("Welcome to A1 OS Edge Layer.", { status: 200 });
});
