#!/usr/bin/env bash
set -e

# SwapForQute Installation Script
# Downloads the latest script from the default branch and sets up the userscript

INSTALL_DIR="${HOME}/.config/qutebrowser/userscripts"
SCRIPT_NAME="sfq.py"
SCRIPT_URL="https://raw.githubusercontent.com/gicrisf/swapforqute/main/${SCRIPT_NAME}"

echo "SwapForQute Installation"
echo "========================"
echo ""

# Check if curl or wget is available
if command -v curl &> /dev/null; then
    DOWNLOAD_CMD="curl -L -o"
elif command -v wget &> /dev/null; then
    DOWNLOAD_CMD="wget -O"
else
    echo "Error: Neither curl nor wget found. Please install one of them and try again."
    exit 1
fi

# Create installation directory
echo "Creating installation directory: ${INSTALL_DIR}"
mkdir -p "${INSTALL_DIR}"

# Download the script
echo "Downloading latest script..."
cd "${INSTALL_DIR}"
${DOWNLOAD_CMD} "${SCRIPT_NAME}" "${SCRIPT_URL}"

# Make executable
echo "Making script executable..."
chmod +x "${SCRIPT_NAME}"

echo ""
echo "Installation complete!"
echo ""
echo "Script installed to: ${INSTALL_DIR}/${SCRIPT_NAME}"
echo ""
echo "Next steps:"
echo "1. Edit the RULES dictionary in ${INSTALL_DIR}/${SCRIPT_NAME} to customize URL transformations"
echo "2. Add to your qutebrowser config.py:"
echo ""
echo "   sfq_script_path = \"~/.config/qutebrowser/userscripts/sfq.py\""
echo "   sfq_cmd = \"--userscript {}\".format(sfq_script_path)"
echo "   c.aliases['sfq'] = \"set-cmd-text -s :spawn {} --cmd 'open' -u \".format(sfq_cmd)"
echo "   config.bind('o', ':sfq')"
echo ""
echo "3. Restart qutebrowser and press 'o' to use SwapForQute!"
echo ""
