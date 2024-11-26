"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var openai_1 = require("openai");
var client = new openai_1.default({
    apiKey: process.env.OPENAI_KEY,
});
function analysisLeverCoffeePressure(args) {
    console.log("Overall score: ", args.score);
    console.log("Comments: ", args.comment);
    console.log("Revise Pressure Chart: ", args.pressure);
}
var definitions = [
    {
        name: "analysisLeverCoffeePressure",
        description: "analysis the pressure",
        parameters: {
            type: "object",
            properties: {
                score: {
                    type: "number",
                    description: "Overall score"
                },
                comment: {
                    type: "string",
                    description: "Comments"
                },
                pressure: {
                    type: "array",
                    items: {
                        type: "number",
                        description: "Pressure Chart"
                    }
                }
            },
            required: ["score", "comment", "pressure"],
        },
    },
];
client.chat.completions
    .create({
    model: "gpt-3.5-turbo",
    messages: [
        {
            role: "system",
            content: "For a given coffee name and pressure and time data, if this is the pressure change when I make the coffee using a lever coffee machine, please analyze it.",
        },
        {
            role: "user",
            content: "espresso, Time (seconds): [0, 5, 10, 15, 20, 25, 30], Pressure (bars): [0, 3, 6, 9, 9, 6, 9]",
        },
    ],
    function_call: "auto", // "auto" is default but we'll make it explicit
    functions: definitions,
})
    .then(function (data) {
    var funcArgs = JSON.parse(data.choices[0].message.function_call.arguments);
    return analysisLeverCoffeePressure(funcArgs);
});
