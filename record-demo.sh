#!/bin/bash
# Sentinel Agent Demo Recorder
# Records terminal session running the agent for demo video

set -e

echo "🎬 Sentinel Agent Demo Recorder"
echo "================================"
echo ""

# Check if OBS is available
if command -v obs &> /dev/null; then
    echo "✅ OBS Studio found"
    OBS_AVAILABLE=true
else
    echo "⚠️  OBS Studio not found"
    echo "   Install: sudo apt install obs-studio"
    echo ""
    echo "Alternative: Using terminal recorder (asciinema)"
    OBS_AVAILABLE=false
fi

# Check if asciinema is available
if command -v asciinema &> /dev/null; then
    echo "✅ asciinema found"
    ASCIINEMA_AVAILABLE=true
else
    echo "⚠️  asciinema not found"
    echo "   Install: sudo apt install asciinema"
    ASCIINEMA_AVAILABLE=false
fi

echo ""
echo "📹 Recording Options:"
echo "1. Manual screen recording (OBS/Screen capture)"
echo "2. Terminal recording (asciinema)"
echo "3. Skip recording, just run demo live"
echo ""
read -p "Choose option (1/2/3): " choice

case $choice in
    1)
        echo ""
        echo "🎥 Starting manual screen recording..."
        echo "Please start OBS/screen recorder now..."
        sleep 5
        
        echo ""
        echo "▶️  Running Sentinel Agent demo..."
        cd /home/user/.openclaw/workspace/web3/coti-challenge
        python3 sentinel_agent.py
        
        echo ""
        echo "⏹️  Stop your screen recorder now!"
        echo "💾 Save video as: sentinel-agent-demo.mp4"
        ;;
        
    2)
        if [ "$ASCIINEMA_AVAILABLE" = false ]; then
            echo "❌ asciinema not installed. Please install or choose option 1."
            exit 1
        fi
        
        echo ""
        echo "📼 Starting terminal recording..."
        cd /home/user/.openclaw/workspace/web3/coti-challenge
        
        # Record the demo
        asciinema rec --title "Sentinel Agent Demo" \
                      --command "python3 sentinel_agent.py" \
                      /tmp/sentinel-demo.cast
        
        echo ""
        echo "✅ Recording saved to: /tmp/sentinel-demo.cast"
        echo "🎬 Convert to video:"
        echo "   asciicast2gif /tmp/sentinel-demo.cast demo.gif"
        echo "   Or upload to: https://asciinema.org"
        ;;
        
    3)
        echo ""
        echo "▶️  Running live demo (no recording)..."
        cd /home/user/.openclaw/workspace/web3/coti-challenge
        python3 sentinel_agent.py
        ;;
        
    *)
        echo "❌ Invalid option"
        exit 1
        ;;
esac

echo ""
echo "================================"
echo "🎉 Demo complete!"
echo ""
echo "Next steps:"
echo "1. Edit video (add intro/outro, captions)"
echo "2. Upload to YouTube/Loom"
echo "3. Post on X tagging @COTInetwork"
echo "4. Submit at stay.coti.io/vibe-coding"
echo ""
