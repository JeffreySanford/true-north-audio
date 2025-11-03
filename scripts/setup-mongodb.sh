#!/bin/bash

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                                                                ║"
echo "║              🗄️  MONGODB MEMORY SERVER SETUP                   ║"
echo "║                                                                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

echo "📦 Initializing MongoDB Memory Server..."
echo "  ℹ️  This will download MongoDB binary (~600MB) on first run"
echo "  ℹ️  Binary is cached, so this only happens once"
echo ""

# Create a temporary test script that triggers MongoDB download
cat > /tmp/test-mongodb.js << 'EOF'
const { MongoMemoryServer } = require('mongodb-memory-server');

async function setup() {
  console.log('Starting MongoDB Memory Server download...');
  const mongod = await MongoMemoryServer.create({
    binary: {
      downloadDir: process.env.HOME + '/.cache/mongodb-binaries',
    }
  });
  
  console.log('MongoDB Memory Server ready!');
  console.log('URI:', mongod.getUri());
  
  await mongod.stop();
  console.log('Setup complete!');
  process.exit(0);
}

setup().catch(err => {
  console.error('Setup failed:', err);
  process.exit(1);
});
EOF

# Run the setup script
START_TIME=$(date +%s)

node /tmp/test-mongodb.js 2>&1 | while IFS= read -r line; do
  if [[ $line == *"Downloading MongoDB"* ]]; then
    echo "  ⏳ $line"
  elif [[ $line == *"ready"* ]] || [[ $line == *"complete"* ]]; then
    echo "  ✅ $line"
  elif [[ $line == *"error"* ]] || [[ $line == *"failed"* ]]; then
    echo "  ❌ $line"
  fi
done

END_TIME=$(date +%s)
SETUP_TIME=$((END_TIME - START_TIME))

# Cleanup
rm -f /tmp/test-mongodb.js

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║              ✅ MONGODB SETUP COMPLETE                         ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
printf "  ⏱️  Setup time: %ds\n" "$SETUP_TIME"
echo "  ℹ️  MongoDB binary cached for future use"
echo ""
