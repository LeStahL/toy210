# toy210 - the team210 live shader editor
#
# Copyright (C) 2018  Alexander Kraus <nr4@z10.info>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

cmake_minimum_required(VERSION 2.8)

project(Toy210)

# Generate ui
set(TOY210_UI
    MainWindow
    GFXPage
    SFXPage
    PreferencesDialog
)
set(TOY210_UIPY)
foreach(ui IN ITEMS ${TOY210_UI})
    message("Generating Ui File: Ui${ui}.py.")
    add_custom_command(OUTPUT Ui${ui}.py
        WORKING_DIRECTORY ${PROJECT_SOURCE_DIR}
        COMMAND pyuic5 ${ui}.ui -o Ui${ui}.py
        DEPENDS "${ui}.ui"
    )
    set(TOY210_UIPY ${TOY210_UIPY} Ui${ui}.py)
endforeach(ui)

# Main target
add_custom_target(toy210 
    ALL
    WORKING_DIRECTORY ${PROJECT_SOURCE_DIR}
    DEPENDS ${TOY210_UIPY}
)
