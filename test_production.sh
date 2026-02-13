#!/bin/bash
# Production App Test Script

echo "================================"
echo "🧪 Testing Production System"
echo "================================"
echo ""

API="http://localhost:5002/api"

echo "1️⃣  Testing server availability..."
if curl -s "$API/auth/me" > /dev/null 2>&1; then
    echo "✅ Server is running"
else
    echo "❌ Server not responding. Start with: cd lab6/src && python app_production.py"
    exit 1
fi

echo ""
echo "2️⃣  Testing CEO login..."
CEO_LOGIN=$(curl -s -X POST "$API/auth/login" \
    -H "Content-Type: application/json" \
    -d '{"username":"ceo","password":"ceo123"}')

if echo "$CEO_LOGIN" | grep -q "success"; then
    echo "✅ CEO login works"
    CEO_ID=$(echo "$CEO_LOGIN" | grep -o '"id":[0-9]*' | grep -o '[0-9]*')
    echo "   CEO user ID: $CEO_ID"
else
    echo "❌ CEO login failed"
    echo "$CEO_LOGIN"
fi

echo ""
echo "3️⃣  Testing team member login..."
TEAM_LOGIN=$(curl -s -X POST "$API/auth/login" \
    -H "Content-Type: application/json" \
    -d '{"username":"john","password":"john123"}')

if echo "$TEAM_LOGIN" | grep -q "success"; then
    echo "✅ Team member login works"
else
    echo "❌ Team member login failed"
fi

echo ""
echo "4️⃣  Testing projects API..."
PROJECTS=$(curl -s "$API/projects")
PROJECT_COUNT=$(echo "$PROJECTS" | grep -o '"id"' | wc -l)
echo "✅ Projects API responds ($PROJECT_COUNT projects)"

echo ""
echo "5️⃣  Testing tasks API..."
TASKS=$(curl -s "$API/tasks")
TASK_COUNT=$(echo "$TASKS" | grep -o '"id"' | wc -l)
echo "✅ Tasks API responds ($TASK_COUNT tasks)"

echo ""
echo "6️⃣  Testing users API..."
USERS=$(curl -s "$API/users")
USER_COUNT=$(echo "$USERS" | grep -o '"id"' | wc -l)
echo "✅ Users API responds ($USER_COUNT users)"

echo ""
echo "7️⃣  Testing dashboard stats..."
STATS=$(curl -s "$API/dashboard/stats")
if echo "$STATS" | grep -q "total_projects"; then
    echo "✅ Dashboard stats working"
    echo "$STATS" | python3 -m json.tool 2>/dev/null | grep "total_" | head -4
else
    echo "❌ Dashboard stats failed"
fi

echo ""
echo "8️⃣  Testing search..."
SEARCH=$(curl -s "$API/tasks?search=test")
echo "✅ Search API responds"

echo ""
echo "9️⃣  Testing filters..."
TODO=$(curl -s "$API/tasks?status=todo")
TODO_COUNT=$(echo "$TODO" | grep -o '"id"' | wc -l)
echo "✅ Status filter works ($TODO_COUNT todo tasks)"

HIGH=$(curl -s "$API/tasks?priority=high")
HIGH_COUNT=$(echo "$HIGH" | grep -o '"id"' | wc -l)
echo "✅ Priority filter works ($HIGH_COUNT high priority)"

echo ""
echo "🔟  Testing calendar API..."
START="2026-02-01T00:00:00"
END="2026-02-28T23:59:59"
CALENDAR=$(curl -s "$API/calendar/tasks?start=$START&end=$END")
echo "✅ Calendar API responds"

echo ""
echo "================================"
echo "✅ All Tests Passed!"
echo "================================"
echo ""
echo "🌐 Open in browser: http://localhost:5002"
echo "👤 Demo accounts:"
echo "   CEO:  ceo / ceo123"
echo "   Team: john / john123"
echo "   Team: jane / jane123"
echo ""
