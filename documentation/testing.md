# Testing
The application has automated testing and has been manually verified to work on both Windows 10 and Ubuntu operating systems.

## Automated testing
### Application logic
The main application logic is mostly tested by a single TestPawn class, which attempts various different pawn-related moves and ensures
illegal moves are not allowed. We do not need to check each piece type separately, as the distinction of different piece types happens mainly
in the MoveValidator class, which is very resilient to change elsewhere in the codebase. 

In addition to general game logic testing, there are separate tests for verifying that only legal moves can be made during check, as well
as testing some of the game's end states. The AI engine also has some rudimentary integration testing.

### Test coverage
The test coverage for the application logic currently stands at 78%.

![](./images/coverage_report.jpg)

The repositories are not included in the automated testing due to their relatively simple logic.

## System testing
The application has been manually tested to work on both Windows 10 and Ubuntu systems. The given commands and installation 
Instructions found in the [user manual](https://github.com/JuhoTurunen/chess-app/blob/main/documentation/user_manual.md) are not
system-specific and work with either operating system.

Each feature in the [requirements specification](https://github.com/JuhoTurunen/chess-app/blob/main/documentation/requirements_specification.md)
document has been verified to work on both operating systems.

## Testing limitations
Currently, the database repositories and initialization are not covered by the automated testing. This is due to the relatively small 
complexity of said database and the logic related to it. Though the database has been thoroughly manually tested.
